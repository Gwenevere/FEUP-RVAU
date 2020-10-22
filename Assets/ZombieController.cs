using UnityEngine;
using UnityEngine.AI;

public class ZombieController : MonoBehaviour
{
    public Camera cam;

    public NavMeshAgent agent;

    private void Start()
    {
        GameObject go = new GameObject("Target");
        Vector3 sourcePostion = new Vector3(100, 20, 100);//The position you want to place your agent
        NavMeshHit closestHit;
        if (NavMesh.SamplePosition(sourcePostion, out closestHit, 500, 1))
        {
            go.transform.position = closestHit.position;
            go.AddComponent<NavMeshAgent>();
            //TODO
        }
        else
        {
            Debug.Log("...");
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
                agent.SetDestination(hit.point);

            }
        }
    }
}
