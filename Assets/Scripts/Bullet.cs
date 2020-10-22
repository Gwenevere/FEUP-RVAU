using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bullet : MonoBehaviour
{
	public float speed;
	public int damage;
    private float timer;
    private Vector3 dir = new Vector3(1,0,0);

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;

        transform.Translate(dir.normalized * speed * Time.deltaTime);

        if(timer > 3)
        {
            Destroy(gameObject);
        }
    }

    void OnTriggerEnter(Collider collider)
    {
        Debug.Log("Bullet collided");

        Destroy(gameObject);
    }

    /*
	public void Seek (Transform _target)
	{
		target = _target;
	}*/
}
