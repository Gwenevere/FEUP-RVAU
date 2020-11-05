using UnityEngine;
using UnityEngine.AI;

public class ZombieController : MonoBehaviour
{
    public NavMeshAgent agent;
    private GameObject target;
    private Vector3 destination;
    public int health;
    private bool walking = false;
    private bool isAttacking = false;
    private Animator animator;
    private int damage = 10;
    private int value = 50;
    EnemySpawner enemySpawner;

    private void Start()
    {
        enemySpawner = GameObject.Find("EnemyController").GetComponent<EnemySpawner>();
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
           

            //agent.SetDestination(destination);

       // }
    }

    void OnCollisionEnter(Collision collision)
    {

    }


    void OnTriggerEnter(Collider collider)
    {
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
        target.GetComponent<Base>().TakeDamage(damage);
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
        enemySpawner.num_zombies--;
        Logger.Log("num_zombies");
        Logger.Log(enemySpawner.num_zombies);
        if(enemySpawner.num_zombies <= 0)
        {
            enemySpawner.StopWave();
        }
        enemySpawner.zombies.Remove(this);
        GameController.Instance.money += value;
        GameController.Instance.ZombieKilled();
        Destroy(gameObject);
    }
    
    void StartMoving()
    {
        agent.SetDestination(destination);
        agent.isStopped = false;
        walking = true;

    }

    void StopMoving()
    {
        agent.isStopped = true;
        walking = false;
    }

}
