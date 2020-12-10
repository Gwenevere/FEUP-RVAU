using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Turret : MonoBehaviour
{
    private GameObject target;
    public int health = 200;
    public float radius;
    public float fireRate = 1f;
    public float level = 1;
    public GameObject bullet;
    private float shoot_timer = 0;
    public Transform firePoint;
    private Vector3 dir;
    private bool shooting = false;
    
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("started turret");
    }

    // Update is called once per frame
    void Update()
    {
        target = FindClosestEnemy();
        Shoot();
        CheckHealth();
        RotateToTarget();
    }

    void CheckHealth()
    {
        if(health<=0)
        {
            //Die
            GameObject.Destroy(gameObject);
        }
    }

    void TakeDamage(int damage)
    {
        health -= damage;
    }


    void Shoot()
    {
        if(shooting && target != null)
        {
            shoot_timer += Time.deltaTime;
            if(shoot_timer > 1/fireRate){
                //Debug.Log("Shoot");
                GameObject new_bullet = Instantiate(bullet, firePoint.position, firePoint.rotation);
                new_bullet.GetComponent<Bullet>().SetTarget(target);
                shoot_timer = 0;
            }
        }
    }

    void RotateToTarget()
    {
        if(target != null)
        {
            dir = target.transform.position - transform.position;
            Quaternion lookDir = Quaternion.LookRotation(dir);
            Vector3 rotation = Quaternion.Lerp(transform.rotation, lookDir, Time.deltaTime).eulerAngles;
            transform.rotation = Quaternion.Euler(0f, rotation.y, 0f);
        }
        
    }
    GameObject FindClosestEnemy() {
        GameObject[] gos;
        gos = GameObject.FindGameObjectsWithTag("Zombie");
        GameObject closest = null;
        float distance = Mathf.Infinity;
        Vector3 position = transform.position;
        foreach (GameObject go in gos) {
            Vector3 diff = go.transform.position - position;
            float curDistance = diff.sqrMagnitude;
            if (curDistance < radius && curDistance < distance) {
                closest = go;
                distance = curDistance;
            //    targetLocation = closest.GetComponent<Vector3> ();
 
        //        Vector3 targetLocation = closest.transform.position;
 
            }
        }
        if(closest != null)
        {
            shooting = true;
        }
        return closest;
        //targetLocation = closest.GetComponent<Vector3> ();
 
        //Vector3 targetLocation = closest.GetComponent<Vector3> ();
    }
    
}
