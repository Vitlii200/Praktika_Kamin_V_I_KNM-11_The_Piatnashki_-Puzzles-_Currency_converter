using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;
public class Puzzle : MonoBehaviour
{
    // Start is called before the first frame update
    public NumberBox numberBox;
    public NumberBox[,] boxes = new NumberBox[4, 4];
    public Sprite[] sprites;
    public List<int> randoms = new List<int>();
    public Text gameText;
    bool VictoryGame;
    void Start()
    {
        VictoryGame = false;
        gameText.text = "не всі числа в правильному порядку";
        randoms.Clear();
        _Init();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    void _Init()
    {
        int n = 0;
        for(int y = 3; y>=0; y--)
        {
            for(int x = 0; x<4; x++)
            {
                n = RandomIndex();
                NumberBox box = Instantiate(numberBox, new Vector2(x, y), Quaternion.identity);
                box.Init(x, y, n+1, sprites[n], ClickToSwap);
                boxes[x, y] = box;
                
            }
        }
    }
    public int RandomIndex()
    {
        int i = Random.Range(0, 16);
        bool isTrue = true;
        if (randoms.Count == 0)
        {
            randoms.Add(i);
            return i;
        }
        else
        {
            while(isTrue)
            {
                foreach (int n in randoms)
                {
                    if (i == n)
                    {
                        isTrue = true;
                        break;
                    }
                    else
                    {
                        isTrue = false;
                    }
                }
                if(isTrue)
                {
                    i = Random.Range(0, 16);
                }
            }
            randoms.Add(i);
            return i;
        }
    }
    void ClickToSwap(int x, int y)
    {
        int dx = getDX(x, y);
        int dy = getDY(x, y);
        var from  = boxes[x, y];
        var target = boxes[x+ dx, y+dy];
        boxes[x, y] = target;
        boxes[x + dx, y + dy] = from;
        from.UpdatePos(x + dx, y + dy);
        target.UpdatePos(x, y);
        int n = 1;
        for (int i = 3; i >= 0; i--)
        {
            for (int k = 0; k < 4; k++)
            { 
                if (boxes[k, i].index == n)
                {
                    VictoryGame = true;
                    n++;
                }
                else if(boxes[k, i].index != n)
                {
                    VictoryGame = false;
                    break;
                }
          
               
            }
            
            if(!VictoryGame)
            {
                break;
            }
            
        }
        if(VictoryGame)
        {
            gameText.text = "Виграв";
        }
    }
    int getDX(int x, int y)
    {
        if(x<3 && boxes[x+1,y].IsEmpty())
        {
            return 1;
        }
        if (x > 0 && boxes[x - 1, y].IsEmpty())
        {
            return -1;
        }
        return 0;
    }
    int getDY(int x, int y)
    {
        if (y < 3 && boxes[x, y+1].IsEmpty())
        {
            return 1;
        }
        if (y > 0 && boxes[x, y-1].IsEmpty())
        {
            return -1;
        }
        return 0;
    }
}
