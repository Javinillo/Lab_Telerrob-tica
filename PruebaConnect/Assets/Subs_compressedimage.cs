using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using UnityEngine.UI;

public class CameraImageSubscriber : MonoBehaviour
{
    public string topicName = "/robot192168118206/compressedimage";  // Tópico de la cámara con imagen comprimida
    public Image canvasImage;  // La imagen que se mostrará en el Canvas 3D (Elemento UI)
    private Texture2D texture;  // Textura donde se cargará la imagen

    // Start is called before the first frame update
    void Start()
    {
        // Conexión con ROS
        var ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<CompressedImageMsg>(topicName, ReceiveCompressedImage);

        // Crear una textura para mostrar la imagen
        texture = new Texture2D(2, 2, TextureFormat.RGB24, false);
    }

    // Función que recibe el mensaje de la imagen comprimida
    void ReceiveCompressedImage(CompressedImageMsg msg)
    {
        // Los datos de la imagen comprimida en formato binario
        byte[] imageData = msg.data;

        // Cargar los datos comprimidos en una textura
        texture.LoadImage(imageData);  // Descomprime los bytes y carga la imagen en la textura
        texture.Apply();  // Aplica la textura

        // Convertir la textura en un Sprite
        Sprite sprite = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), new Vector2(0.5f, 0.5f));

        // Asignar el Sprite a la imagen en el Canvas
        canvasImage.sprite = sprite;
    }
}

