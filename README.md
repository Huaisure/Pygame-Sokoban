# Pygame Sokoban

### 班级：自11 学号：2021013433 姓名：刘淮硕

## 项目背景

推箱子游戏，实现以下两个任务：

（1） 任务一：箱子被推到洞口后不会消失（可以再次被推出来），且箱子和洞口不存在一一对应的关系，设计一种搜索算法，找到最优的移动路线（人物移动的次数最少）。

（2） 任务二：箱子被推到洞口后会消失，且箱子和洞口一一对应，设计一种搜索算法，找到最优的移动路线

## 实现思路

python实现，使用pygame库搭建界面。

代码主要分为两个模块，分别为 assests 和 solution ，assets模块中为游戏相关的内容，主要为Game类，含有读取地图，绘制地图，更新地图等功能；solution 模块中为搜索算法，分别为任务一对应的 Solution 类，与任务二对应的 Solution_plus 类，采用 A* 算法，代价函数为步数，启发式函数为曼哈顿距离（具体来说，任务一为每个箱子到目标最小曼哈顿距离和，任务二为每个箱子到各自目标的曼哈顿距离和）。

具体搜索的思路为，状态为 `(cur_player_pos, cur_boxes) `，对于游戏中的所有元素，只有玩家当前位置与箱子位置是可变的，其余的元素均为不变的量，所以将这两者作为状态是合理的；维护一个优先级队列，根据每个状态的代价函数与启发式函数之和排序，可以更快的找到最优解。

Solution_plus 沿用任务一的思路，在许多细节处做了修改，比如启发式函数的计算方式，或者寻找当前状态所有可能的下一个状态时，有所修改，具体内容详见代码。

## How to use it

在项目根目录下，python环境下安装项目所需的依赖：

```shell
pip install -r requirements.txt
```

同样的，在根目录下

``` shell
python main.py
```

按照终端中的要求输入对应的任务和关卡即可。生成路径可能需要不超过10秒的时间，在未生成完前，图形界面不会生成，请耐心等待一会。

目前不支持手动移动玩家，只能展示自动移动的结果。

## 效果

这里展示一张移动过程中的图片，这里是任务一玩家在移动箱子的过程。

![alt text](image.png)
