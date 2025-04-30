#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

# Inicializa los valores
scale = 100
quality = 50
ipg = 1000
rotation_angle = 0

# Parámetros de movimiento del robot
linear_speed = 0.2  # Velocidad lineal base (aumentado)
angular_speed = 0.5 # Velocidad angular base
twist = Twist()
last_key = None  # Última tecla presionada

# Publicadores de ROS
publis_size = rospy.Publisher('/robot1921681092/changeSize', Int32, queue_size=10)
publis_quality = rospy.Publisher('/robot1921681092/changeQuality', Int32, queue_size=10)
publis_ipg = rospy.Publisher('/robot1921681092/changeTimeInterFrames', Int32, queue_size=10)
publis_cmd_vel = rospy.Publisher('/robot1921681092/cmd_vel', Twist, queue_size=10)

def update_parameters(changed, action=""):
    """
    Publica los valores actualizados en los tópicos de ROS.
    Muestra un mensaje solo si se ha cambiado algún valor.
    """
    if changed:
        publis_size.publish(scale)
        publis_quality.publish(quality)
        publis_ipg.publish(ipg)
        rospy.loginfo(f"[ACTION] {action} | Scale: {scale}, Quality: {quality}, IPG: {ipg}")

def process_key(key):
    """
    Procesa la tecla presionada y ajusta los parámetros en consecuencia.
    """
    global scale, quality, ipg, rotation_angle, twist, last_key
    changed = False  # Variable para rastrear si hubo cambios
    action = ""  # Mensaje de la acción realizada

    # Configuración de escala, calidad, IPG y rotación
    if key == ord('i'):  # Incrementar escala
        if scale < 100:
            scale += 10
            changed = True
            action = "Increased Scale"
    elif key == ord('k'):  # Disminuir escala
        if scale > 10:
            scale -= 10
            changed = True
            action = "Decreased Scale"
    elif key == ord('o'):  # Incrementar calidad
        if quality < 100:
            quality += 10
            changed = True
            action = "Increased Quality"
    elif key == ord('l'):  # Disminuir calidad
        if quality > 10:
            quality -= 10
            changed = True
            action = "Decreased Quality"
    elif key == ord('u'):  # Incrementar IPG
        ipg += 100
        changed = True
        action = "Increased IPG"
    elif key == ord('j'):  # Disminuir IPG
        if ipg > 100:
            ipg -= 100
            changed = True
            action = "Decreased IPG"
    elif key == ord('n'):  # Rotar a la izquierda
        rotation_angle = (rotation_angle - 90) % 360
        changed = True
        action = "Rotated Left"
    elif key == ord('m'):  # Rotar a la derecha
        rotation_angle = (rotation_angle + 90) % 360
        changed = True
        action = "Rotated Right"

    # Control de movimiento del robot
    if key == ord('w'):  # Avanzar
        twist.linear.x = linear_speed
        twist.angular.z = 0.0
        action = "Moving Forward"
    elif key == ord('s'):  # Retroceder
        twist.linear.x = -linear_speed
        twist.angular.z = 0.0
        action = "Moving Backward"
    elif key == ord('a'):  # Girar a la izquierda
        twist.linear.x = 0.0
        twist.angular.z = angular_speed
        action = "Turning Left"
    elif key == ord('d'):  # Girar a la derecha
        twist.linear.x = 0.0
        twist.angular.z = -angular_speed
        action = "Turning Right"
    elif key == ord('q'):  # Desplazarse a la izquierda
        twist.linear.y = linear_speed
        twist.angular.z = 0.0
        action = "Strafing Left"
    elif key == ord('e'):  # Desplazarse a la derecha
        twist.linear.y = -linear_speed
        twist.angular.z = 0.0
        action = "Strafing Right"
    elif key == 32:  # Barra espaciadora (detener)
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.angular.z = 0.0
        action = "Stopping"

    # Publica el mensaje de velocidad si la tecla cambió
    if key != last_key:
        publis_cmd_vel.publish(twist)
        rospy.loginfo(f"[ACTION] {action}")
        last_key = key  # Guarda la última tecla presionada

    # Actualiza parámetros si hubo cambios
    update_parameters(changed, action)

def image_callback(msg):
    """
    Callback que recibe la imagen, la procesa y muestra.
    """
    try:
        np_arr = np.frombuffer(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except CvBridgeError as e:
        rospy.logerr(e)
        return
    
    # Rotar imagen
    if rotation_angle != 0:
        if rotation_angle == 90:
            image_np = cv2.rotate(image_np, cv2.ROTATE_90_CLOCKWISE)
        elif rotation_angle == 180:
            image_np = cv2.rotate(image_np, cv2.ROTATE_180)
        elif rotation_angle == 270:
            image_np = cv2.rotate(image_np, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    # Mostrar imagen
    cv2.namedWindow('cv_img', cv2.WINDOW_NORMAL)
    cv2.imshow('cv_img', image_np)
    
    # Obtener entrada del teclado
    key = cv2.waitKey(50) & 0xFF
    process_key(key)

def main():
    rospy.init_node('image_processing')
    image_topic = "/robot1921681092/compressedimage"
    rospy.Subscriber(image_topic, CompressedImage, image_callback)
    
    # Mantener la publicación de `cmd_vel` para que el robot no se detenga
    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        publis_cmd_vel.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    main()

