# airdrop

 Think of it like a virtual sandbox where we can test out different ways of giving away tokens and see what happens to the token's value.

## What does this code do?

Imagine you're launching a new cryptocurrency and want to give some tokens away to early users. This is called an "airdrop". But how you do that airdrop can make a big difference to how people use the token and what it's worth.

This code lets us simulate a token economy with different airdrop strategies. It models:

*   **Users:** We have different types of users (like speculators, long-term holders, airdrop hunters, and active users), each with their own tendencies to buy or sell tokens.
*   **Token Price:** The price of the token changes based on how much people are buying and selling.
*   **Airdrops:** We can simulate different ways of distributing the tokens, such as:
    *   **Lottery:** Randomly selecting winners to receive tokens.
    *   **Uniform:** Giving the same amount of tokens to everyone.
    *   **Tiered:** Giving different amounts of tokens based on how much a user already holds or how active they are.
    *   **Vesting:**  Releasing the airdropped tokens over time, sometimes depending on certain conditions being met (like the token price going up or the user being active).
*   **Market Behavior:** Users make decisions to buy or sell tokens based on factors like the current price, how they feel about the market, and the specific airdrop strategy being used.
*   **Token Supply:** The total number of tokens in circulation can change due to a "burn" mechanism (a small percentage of tokens is removed from circulation with each transaction).

The code runs a simulation for each different airdrop strategy we define. It tracks the token price over time and the final total supply of tokens. This lets us compare which airdrop strategies might be more effective at increasing the token's value or influencing the token's economy in other ways.

## Why is this useful?

By simulating these different scenarios, we can get a better understanding of the potential consequences of different airdrop strategies *before* actually implementing them. This can help in designing more effective and sustainable token distribution mechanisms.

## Want to know the details?

If you're interested in the more technical details of how the simulation works, including the mathematical formulas and models used, you can check out the accompanying document: [`math.md`](math.md). This document explains the mathematical underpinnings of the simulation.

## Running the code

The Python code (`main.py`) will run the simulations and generate a CSV file (`airdrop_simulation_results.csv`) containing the results for each airdrop strategy. It will also display a graph showing the token price over time for each strategy.

This project is a simplified model of a complex system, but it provides a valuable tool for exploring the dynamics of cryptocurrency airdrops.
