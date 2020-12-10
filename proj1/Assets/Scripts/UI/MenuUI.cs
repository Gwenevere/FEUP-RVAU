using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class MenuUI : MonoBehaviour
{
    public GameObject warningText;
    private GameObject nextText;
    private Coroutine fadeCoroutine;
    
    // Start is called before the first frame update
    void Start() {}

    // Update is called once per frame
    void Update() {}

    public void NoBaseWarning()
    {
        if(fadeCoroutine != null)
        {
            StopCoroutine(fadeCoroutine);
        }
        if(nextText != null)
        {
            GameObject.Destroy(nextText);
        }
        nextText = Instantiate(warningText, warningText.transform.position, Quaternion.identity);
        nextText.transform.SetParent(gameObject.transform);
        nextText.SetActive(true);
        fadeCoroutine = StartCoroutine(FadeOutRoutine());
    }

    private IEnumerator FadeOutRoutine()
    { 
        Text text = nextText.GetComponent<Text>();
        Color originalColor = text.color;
        for (float t = 0.01f; t < 2; t += Time.deltaTime)
        {
            text.color = Color.Lerp(originalColor, Color.clear, Mathf.Min(1, t/3));
            yield return null;
        }
        if(nextText != null)
        {
            GameObject.Destroy(nextText);
        }
    }
}
