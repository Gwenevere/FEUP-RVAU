using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bullet : MonoBehaviour
{
	public float speed;
	public int damage;
    private float timer;
    private Vector3 dir;
    GameObject target;

    // Start is called before the first frame update
    void Start()
    {
    }

    public void SetTarget(GameObject target_turret)
    {
        target = target_turret;
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;

        if(target != null)
        {
            dir = target.transform.position - transform.position;
            transform.Translate(dir.normalized * speed * Time.deltaTime, Space.World);
        }
        else
        {
            GameObject.Destroy(gameObject);
        }

    }

    void OnTriggerEnter(Collider collider)
    {
        if (collider.gameObject.tag == "Zombie")
        {
            Destroy(gameObject);
            // zombiecontroller ou outros se houver mais inimigos
            target.GetComponent<ZombieController>().TakeDamage(damage);
        }
    }

    /*
	public void Seek (Transform _target)
	{
		target = _target;
	}*/
}
