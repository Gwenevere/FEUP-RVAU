using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PositionPrinter : MonoBehaviour
{
    public string debug_name;
    public bool active;
    private Vector2 position;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(active)
        {
            Debug.Log("[" + gameObject.name + "] World pos: " + gameObject.transform.position);
            Debug.Log("[" + gameObject.name + "] Local pos: " + gameObject.transform.localPosition);
        }
    }
}
