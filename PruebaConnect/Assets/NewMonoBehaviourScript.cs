using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class CompressedImageSubscriber : MonoBehaviour
{
    public string topicName = "/robot19216839179/compressedimage";  // Tópico de la cámara con imagen comprimida
    public GameObject plane;  // El objeto 3D (por ejemplo, un Quad) donde se mostrará la imagen
    private Renderer planeRenderer;  // Para acceder al material del Quad y aplicar la textura

    private Texture2D texture;

    void Start()
    {
        // Inicializa la conexión ROS
        var ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<CompressedImageMsg>(topicName, ReceiveCompressedImage);
        
        // Encuentra el renderer del objeto 3D donde vamos a aplicar la textura
        planeRenderer = plane.GetComponent<Renderer>();
        
        // Crea una textura para mostrar la imagen
        texture = new Texture2D(2, 2, TextureFormat.RGB24, false);
    }

    // Función para procesar el mensaje de imagen comprimida
    void ReceiveCompressedImage(CompressedImageMsg msg)
    {
        // Los datos de la imagen comprimida en formato binario
        byte[] imageData = msg.data;

        // Cargar los datos comprimidos en una textura
        texture.LoadImage(imageData);  // Descomprime los bytes y carga la imagen en la textura
        texture.Apply();  // Aplica la textura

        // Asigna la textura al material del objeto 3D (Plane o Quad)
        planeRenderer.material.mainTexture = texture;
    }
}

