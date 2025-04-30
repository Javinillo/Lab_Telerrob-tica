#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int32
import numpy as np
import cv2
import os
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

# Inicializa los valores
scale = 100
quality = 50
ipg = 1000
rotation_angle = 0
last_action = ""  # Variable para rastrear la última acción

# Publicadores de ROS
publis_size = rospy.Publisher('/robot1921681092/changeSize', Int32, queue_size=10)
publis_quality = rospy.Publisher('/robot1921681092/changeQuality', Int32, queue_size=10)
publis_ipg = rospy.Publisher('/robot1921681092/changeTimeInterFrames', Int32, queue_size=10)


def update_parameters(changed, action=""):
    """
    Publica los valores actualizados en los tópicos de ROS.
    Muestra un mensaje solo si se ha cambiado algún valor.
    """
    global last_action

    if changed and action != last_action:
        publis_size.publish(scale)
        publis_quality.publish(quality)
        publis_ipg.publish(ipg)
        
        print()
        print(f"Última acción: {action}")
        print(f"Scale: {scale}%")
        print(f"Quality: {quality}%")
        print(f"IPG: {ipg}ms")
        print(f"Rotation: {rotation_angle}°")

        last_action = action  # Guarda la última acción para evitar repeticiones innecesarias

def process_key(key):
    """
    Procesa la tecla presionada y ajusta los parámetros en consecuencia.
    """
    global scale, quality, ipg, rotation_angle
    changed = False  # Variable para rastrear si hubo cambios
    action = ""  # Mensaje de la acción realizada

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
    cv2.imshow('cv_img', image_np)
    key = cv2.waitKey(5) & 0xFF

    # Procesar la tecla presionada
    process_key(key)

def main():
    rospy.init_node('image_processing')
    image_topic = "/robot1921681092/compressedimage"
    rospy.Subscriber(image_topic, CompressedImage, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()

