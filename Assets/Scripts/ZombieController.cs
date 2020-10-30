using UnityEngine;
using UnityEngine.AI;

public class ZombieController : MonoBehaviour
{
    public NavMeshAgent agent;
    private GameObject target;
    private Vector3 destination;
    public int health = 20;
    private bool walking = false;
    private bool isAttacking = false;
    private Animator animator;
    private int damage;

    private void Start()
    {
        damage = 20;
        animator = gameObject.GetComponent<Animator>();
        target = GameObject.Find("Base");
        //agent.Warp(gameObject.transform.position);
        StartMoving();
    }

    // Update is called once per frame
    void Update()
    {
        int threshold = 0;

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
           

            agent.SetDestination(destination);

       // }
    }

    void OnCollisionEnter(Collision collision)
    {
        Debug.Log("colission enter zombie");

    }


    void OnTriggerEnter(Collider collider)
    {
        Debug.Log("trigger  enter zombie");
        //Check for a match with the specified name on any GameObject that collides with your GameObject
        if (collider.gameObject.name == "Base")
        {
            //If the GameObject's name matches the one you suggest, output this message in the console
            Debug.Log("Collided with base!");

            StopMoving();
            StartAttacking();
        }

    }
    
    void StartAttacking()
    {
        isAttacking = true;
        animator.SetBool("isAttacking", true);
    }

    public void DoDamage()
    {
        target.GetComponent<Tower>().TakeDamage(damage);
    }

    public void TakeDamage(int damage)
    {
        health -= damage;
        if(health <= 0)
        {
            Die();
        }
    }

    private void Die()
    {
        Destroy(gameObject);
    }
    
    void StartMoving()
    {
        agent.Move(destination);
        agent.isStopped = false;
        walking = true;

    }

    void StopMoving()
    {
        agent.isStopped = true;
        walking = false;
    }

}
