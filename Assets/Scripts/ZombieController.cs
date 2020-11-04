using UnityEngine;
using UnityEngine.AI;

public class ZombieController : MonoBehaviour
{
    public NavMeshAgent agent;
    private GameObject target;
    private Vector3 destination;
    GameController gameController;
    public int health;
    private bool walking = false;
    private bool isAttacking = false;
    private Animator animator;
    private int damage = 20;
    private int value = 50;

    private void Start()
    {
        Logger.Log("Zombie Spawned");
        animator = gameObject.GetComponent<Animator>();
        target = GameObject.Find("Base");
        //agent.Warp(gameObject.transform.position);
        StartMoving();
    }

    public void Constructor(int n_value, int n_damage, int n_health)
    {
        value = n_value;
        damage = n_damage;
        health = n_health;
        gameObject.transform.localScale = new Vector3(0.08f, 0.07f, 0.08f);
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
        GameController.Instance.money += value;
        gameController.zombiesKilled++;
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
