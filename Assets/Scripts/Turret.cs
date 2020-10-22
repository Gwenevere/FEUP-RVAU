using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Turret : MonoBehaviour
{
    public GameObject target;
    public int health = 200;
    public float fireRate = 4f;
    public float level = 1;
    public GameObject bullet;
    private float shoottimer = 0;
    public Transform firePoint;
    private Vector3 dir;
    
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("started turret");
    }

    // Update is called once per frame
    void Update()
    {
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
        shoottimer += Time.deltaTime;
        if(shoottimer > 1/fireRate){
            Debug.Log("Shoot");
            Instantiate(bullet, firePoint.position, firePoint.rotation);
            shoottimer = 0;
        }
    }

    void RotateToTarget()
    {
        dir = target.transform.position - transform.position;
        Quaternion lookDir = Quaternion.LookRotation(dir);
        Vector3 rotation = Quaternion.Lerp(transform.rotation, lookDir, Time.deltaTime).eulerAngles;
        transform.rotation = Quaternion.Euler(0, rotation.y, 0);
        
    }
    
}
