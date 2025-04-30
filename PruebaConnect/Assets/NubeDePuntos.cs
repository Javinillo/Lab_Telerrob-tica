using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using System;
using System.Collections.Generic;

public class PointCloudSubscriber : MonoBehaviour
{
    public string topicName = "/rtabmap/cloud_map";  // Tópico de la nube de puntos
    public GameObject pointPrefab;  // Prefab de un cubo o esfera para representar cada punto
    public float scaleFactor = 0.05f;  // Factor de escala para los puntos

    private List<GameObject> points = new List<GameObject>();  // Lista para almacenar los puntos

    // Start is called before the first frame update
    void Start()
    {
        // Conexión con ROS
        var ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<PointCloud2Msg>(topicName, ReceivePointCloudData);
    }

    // Función que recibe los datos de la nube de puntos
    void ReceivePointCloudData(PointCloud2Msg msg)
    {
        // Limpia los puntos anteriores
        foreach (GameObject point in points)
        {
            Destroy(point);
        }
        points.Clear();

        // Procesar los datos de la nube de puntos
        int pointCount = msg.data.Length / 16;  // Cada punto tiene 16 bytes: x, y, z (4 bytes por coordenada)

        for (int i = 0; i < pointCount; i++)
        {
            // Obtener las coordenadas de cada punto (XYZ)
            float x = BitConverter.ToSingle(msg.data, i * 16);
            float y = BitConverter.ToSingle(msg.data, i * 16 + 4);
            float z = BitConverter.ToSingle(msg.data, i * 16 + 8);

            // Escalar y crear el objeto del punto
            Vector3 pointPosition = new Vector3(x * scaleFactor, y * scaleFactor, z * scaleFactor);
            GameObject pointObject = Instantiate(pointPrefab, pointPosition, Quaternion.identity);

            // Agregar el objeto a la lista y a la escena
            points.Add(pointObject);
            pointObject.transform.SetParent(transform);
        }
    }
}

