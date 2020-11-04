using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class EnemySpawner : MonoBehaviour
{
    public ZombieController zombie;
    public GameObject imageTarget;
    public float spawn_radius;
    List<ZombieController> zombies;
    int num_zombies;
    int num_wave_zombies;
    int num_courotine = 1;
    private Coroutine currentCoroutine;

    // Start is called before the first frame update
    void Start()
    {
        zombies = new List<ZombieController>();
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
        Logger.Log("Started wave with " + num_wave_zombies);
        currentCoroutine = StartCoroutine(SpawnZombies(time_between));
    }

    public void ResetSpawner()
    {
        if (currentCoroutine != null)
        {
            StopCoroutine(currentCoroutine);
        }

        foreach (GameObject zombie in GameObject.FindGameObjectsWithTag("Zombie"))
        {
            num_zombies--;
            GameObject.Destroy(zombie);
        }

        zombies.Clear();
    }

    public void StopWave()
    {
        ResetSpawner();
        GameController.Instance.NextWave();
    }

    IEnumerator SpawnZombies(float time)
    {
        while(true)
        {
            var newZombie = Instantiate(zombie, GenerateSpawnCoordinates(), Quaternion.identity);
            newZombie.transform.parent = imageTarget.transform;
            //  Change zombie according to wave number
            if(GameController.Instance.current_wave >= 3)
            {
                var r = Random.Range(1,6);
                if(r == 1)
                {
                    newZombie.Constructor(100, 40, 200);
                }
            }

            zombies.Add(newZombie);
            num_zombies++;
            Logger.Log("Zombie Spawned");

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
