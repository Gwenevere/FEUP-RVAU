using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    public ZombieController zombie;
    public float spawn_radius;

    // Start is called before the first frame update
    void Start()
    {
        StartSpawning();    // Depois é o game controller que chama
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void StartSpawning()
    {
        StartCoroutine(SpawnZombie(2f));
    }

    IEnumerator SpawnZombie(float time)
    {
        while(true)
        {
            Logger.Log("Zombie Spawned");
            Instantiate(zombie, GenerateSpawnCoordinates(), Quaternion.identity);
            yield return new WaitForSeconds(time);
        }
    }

    private Vector3 GenerateSpawnCoordinates()
    {
        float angle = Random.Range(0f, Mathf.PI*2);
        float x = Mathf.Cos(angle) * spawn_radius;
        //float y = 0.0004f;
        float y = 0f;
        float z = Mathf.Sin(angle) * spawn_radius;


        return new Vector3(x, y, z);    // y = 0?
    }
}
