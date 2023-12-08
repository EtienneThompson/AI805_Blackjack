This is the repository for our AI805 Blackjack project.

**Authors:**
- [Etienne Thompson](https://github.com/EtienneThompson)
- [Gaven Wolfgang](https://github.com/kidbuu18962)
- [Ju Hyung Kang](https://github.com/Belladonna00)

**Running the code:**

To run the code, run the command:

```bash
python3 blackjack.py
```

It will prompt if you want to run the project in debug mode or simulation mode.

Debug mode runs the series of games, but allows for user interaction to step through the code. It also will output extra logs into the console.

Simulation mode will quickly run through 100 iterations of the game, without waiting for user input, and will output less information to the console.

**What is the project?**

This is an implementation of a blackjack simulator, with three different artificial intelligence algorithms implemented to model the game and make decisions. The goal was to see which algorithm was able to best play blackjack and have the best odds of winning against the dealer. The three algorithms we decided to implement were:
- Game Tree implementation, with expect-minimax variant to search the game tree.
- Q-Learning model, to learn the game as it plays.
- Genetic Algorithm, to evolve an agent to better play over time.