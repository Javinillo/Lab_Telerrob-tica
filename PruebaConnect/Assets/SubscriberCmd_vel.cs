using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.ROSGeometry;
using RosMessageTypes.Geometry; // geometry_msgs/msg/Twist para ROS2

public class SubscriberCmd_vel : MonoBehaviour
{
    public string topicName = "/robot192168118206/cmd_vel";
    public GameObject sphere;
    public float speedMultiplier = 1.0f;

    private ROSConnection ros;
    private Vector3 linearVelocity = Vector3.zero;
    private Vector3 angularVelocity = Vector3.zero;

    void Start()
    {
        // Instancia la conexión ROS
        ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<TwistMsg>(topicName, ReceiveCmdVel);
    }

    void ReceiveCmdVel(TwistMsg msg)
    {
        // Convertir de geometry_msgs/msg/Twist (ROS2) a Vector3
        linearVelocity = new Vector3((float)msg.linear.x, (float)msg.linear.y, (float)msg.linear.z);
        angularVelocity = new Vector3((float)msg.angular.x, (float)msg.angular.y, (float)msg.angular.z);
    }

    void Update()
    {
		if (sphere != null)
		{
		    // Avanza en la dirección actual
		    Vector3 forwardVelocity = sphere.transform.forward * linearVelocity.z * speedMultiplier;
		    Vector3 strafeVelocity = sphere.transform.right * linearVelocity.x * speedMultiplier;
		    Vector3 verticalVelocity = sphere.transform.up * linearVelocity.y * speedMultiplier;

		    sphere.transform.position += (forwardVelocity + strafeVelocity + verticalVelocity) * Time.deltaTime;

		    // Rotación: solo angular.z afecta a giro en plano horizontal (eje Y en Unity)
		    sphere.transform.Rotate(Vector3.up * angularVelocity.z * speedMultiplier * Mathf.Rad2Deg * Time.deltaTime);
		}
    }
}

