using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetChangeHandler : MonoBehaviour
{
    public bool debug_active;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ContentPlacedHandler()
    {
        if(debug_active)
        {
            Debug.Log(" Content placed");
        }
    }

    public void PlaneFoundHandler()
    {
        if(debug_active)
        {
            Debug.Log("Plane was FOUND.");
        }
    }

    public void ImageTargetFoundHandler()
    {
        if(debug_active)
        {
            Debug.Log("Image target was FOUND.");
        }
    }

    public void PlaneLostHandler()
    {
        if(debug_active)
        {
            Debug.Log("Plane was LOST.");
        }
    }

    public void ImageTargetLostHandler()
    {
        if(debug_active)
        {
            Debug.Log("Image target was LOST.");
        }
    }
}
