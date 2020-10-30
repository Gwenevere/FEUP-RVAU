using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class EnemySpawner : MonoBehaviour
{
    public ZombieController zombie;
    public float spawn_radius;
    GameObject[] zombies;
    int num_zombies;
    int num_wave_zombies;
    int num_courotine = 1;
    private Coroutine currentCoroutine;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        num_wave_zombies = GameController.Instance.current_wave * 5;
        //Debug.Log(GameController.Instance.current_wave);
        if(num_zombies > num_wave_zombies)
        {
            StopCoroutine(currentCoroutine);
        }
    }

    public void StartWave()
    {
        float time_between = Random.Range(2,6);
        Debug.Log("Started wave with " + num_wave_zombies);
        currentCoroutine = StartCoroutine(SpawnZombies(time_between));
    }

    public void StopWave()
    {
        StopCoroutine(currentCoroutine);
        foreach (GameObject zombie in GameObject.FindGameObjectsWithTag("Zombie"))
        {
            num_zombies--;
            GameObject.Destroy(zombie);
        }
        GameController.Instance.NextWave();
    }

    IEnumerator SpawnZombies(float time)
    {
        while(true)
        {
            num_zombies++;
            Debug.Log("Zombie Spawned");
            Instantiate(zombie, GenerateSpawnCoordinates(), Quaternion.identity);
            yield return new WaitForSeconds(time);
        }
    }

    private Vector3 GenerateSpawnCoordinates()
    {
        float angle = Random.Range(0f, Mathf.PI*2);
        float x = Mathf.Cos(angle) * spawn_radius;
        float y = 0.0004f;
        float z = Mathf.Sin(angle) * spawn_radius;


        return new Vector3(x, y, z);    // y = 0?
    }
}
