using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Logger : MonoBehaviour
{
    public static void Log(object input)
    {
        Debug.Log("[CUSTOM]: " + input);
    }
}
