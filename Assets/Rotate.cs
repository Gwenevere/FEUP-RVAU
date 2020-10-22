using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotate : MonoBehaviour
{

    private bool updatedBefore = false;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {

       //  if (!updatedBefore)
        {
            this.transform.Translate(new Vector3(0, 0.2f, 0));
        }

        this.transform.Rotate(new Vector3(-90, 0, 0));

        updatedBefore = true;
    }
}
