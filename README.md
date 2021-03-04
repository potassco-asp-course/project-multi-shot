# Multi-shot

Please modify [multi-shot.lp](./multi-shot.lp) with your encoding.
Every time you will push a new commit, your solution will be tested automatically.
After a few minutes you will be able to see the result of the test in the **Actions** tab.
You can get more information  about the result of the test by clicking on:
1. The specific test,
2. "Autograding",
3. "Run education/autograding@v1", and
4. Scrolling down until line ~150.

There, for each instance, you will see if the test is a:
* "success" (correct answer),
* "failure" (wrong answer),
* "timeout" (no solution found before the time runs out)
* "error" (clingo error).

For each instance, you can find the list of all optimal solutions in the [solutions](./solutions) folder.
Your encoding only need to find one optimal solution.
