using UnityEngine;
using UnityEngine.AI;

public class ZombieController : MonoBehaviour
{
    public Camera camera;

    public NavMeshAgent agent;

    public GameObject baseObject;

    private void Start()
    {
        baseObject = GameObject.Find("Base");
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            /* Ray ray = camera.ScreenPointToRay(Input.mousePosition);
             RaycastHit hit;

             if (Physics.Raycast(ray, out hit))
             {
                 agent.SetDestination(hit.point);

             }
             */


        }
    }
}
