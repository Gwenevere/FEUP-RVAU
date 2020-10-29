using UnityEngine;
using UnityEngine.AI;

public class ZombieController : MonoBehaviour
{
    public Camera camera;
    public NavMeshAgent agent;
    private GameObject target;
    private Vector3 destination;

    private bool walking = false;

    private void Start()
    {
        target = GameObject.Find("Base");
        agent.Warp(gameObject.transform.position);
    }

    // Update is called once per frame
    void Update()
    {
        int threshold = 0;

        Logger.Log(Vector3.Distance(this.transform.position, destination));

        //if (walking && Vector3.Distance(this.transform.position, destination) <= threshold)
        //{
        //    Debug.Log("---------------HERE!-----------------");
        //    StopMoving();
        //    // rb.angularVelocity =    ;
        //    // agent.velocity = Vector3.zero;
        //}
        

      //  if (Input.GetMouseButtonDown(0))
       // {
       /*     Ray ray = camera.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
               destination = hit.point;
               agent.SetDestination(destination);
               StartMoving();
            }*/
           

            destination = target.transform.position;
            agent.SetDestination(destination);
            StartMoving();

       // }
    }


    void OnCollisionEnter(Collision collision)
    {
        //Check for a match with the specified name on any GameObject that collides with your GameObject
        if (collision.gameObject.name == "Base")
        {
            //If the GameObject's name matches the one you suggest, output this message in the console
            Debug.Log("Collided!");

            StopMoving();
        }

    }

    void StartMoving()
    {
        agent.isStopped = false;
        walking = true;

    }

    void StopMoving()
    {
        agent.isStopped = true;
        walking = false;
    }

}
