# PRNG

This research focuses on the development and evaluation of novel Pseudorandom Number Generator (PRNG) algorithms for statistical randomness testing. We propose and test several custom PRNG algorithms, designed with specific architectural variations to assess their efficacy in producing random sequences under various statistical tests. The algorithms are evaluated using two standard tests—Kolmogorov-Smirnov (K-S) and Chi-Square—across a range of parameter values, particularly focusing on the value of m, the number of random numbers generated in each sequence. The results of these tests, including both statistical significance and performance metrics, are stored in a database for subsequent analysis and visualization.

Our approach includes the design of PRNGs with distinct mechanisms, such as hybrid models, switch-based generators, and shift-based variations, each aimed at enhancing randomness and mitigating common PRNG flaws. The evaluation is conducted with multithreading support, allowing for efficient parallel testing of multiple algorithms under diverse configurations. Visualization tools are used to analyze the rejections of the null hypothesis, providing a clear comparison of the statistical validity of each algorithm. This research aims to contribute to the field of random number generation by exploring innovative algorithmic designs and assessing their practical applicability through rigorous testing.

In the testing, `HPRNG` [[1]](https://github.com/hind-sagar-biswas/PRNG#References) has been used as base algorithm. It is used as referrence for performance testing.

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/PRNG.git
    cd PRNG
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. **Install required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Or install individual dependencies if necessary:

    ```bash
    pip install numpy scipy matplotlib seaborn pandas
    ```

## Usage

**Run the tests:**

Run the `test.py` script to start the tests for different PRNG algorithms. It will:

1. Generate random numbers for each algorithm at different m values.
2. Perform the Kolmogorov-Smirnov and Chi-Square tests.
3. Store the results in SQLite databases (test_X.db where X is the thread index).
4. Use multithreading to run tests in parallel.
5. Visualize the results.

**Example:**

```bash
python test.py
```

You will be prompted to input:

`Only Rejections (1 = True, 0 = False)`: Choose whether you want to visualize only the rejections or all test results.
`Number of Threads`: Specify how many threads to use for parallel testing.

## Files

1. `test.py`: Main script that runs the PRNG tests, performs statistical tests, and stores results in an SQLite database.
2. `visualize.py`: Script that generates plots and heatmaps based on the test results.
3. `dbconn.py`: Database connection utility for handling SQLite interactions.
4. `algos/`: Directory containing the PRNG algorithm implementations.

## SQLite Database

- The results of the tests are stored in SQLite databases named `test_X.db`, where `X` is the thread index.
- The table RandomnessTests includes the following columns:
    - `ALGO`: The name of the algorithm.
    - `M`: The value of m.
    - `N`: The number of random numbers generated.
    - `ALPHA`: The significance level of the statistical test.
    - `RAND_NUMS`: The random numbers generated.
    - `KS_REJECTED`: Whether the Kolmogorov-Smirnov test rejected the null hypothesis.
    - `CHI_REJECTED`: Whether the Chi-Square test rejected the null hypothesis.
    - `D_STAT`: The Kolmogorov-Smirnov test statistic.
    - `CHI_2_STAT`: The Chi-Square test statistic.
    - `KS_P_VALUE`: The p-value of the Kolmogorov-Smirnov test.
    - `CHI_P_VALUE`: The p-value of the Chi-Square test.
    - `TIME`: The time taken by the algorithm to generate random numbers.

## Dependencies

- Python `3.x`
    - numpy
    - scipy
    - matplotlib
    - seaborn
    - pandas

## Contributing

Feel free to fork the repository, submit issues, and create pull requests.

## License

This project is licensed under the `MIT` License - see the LICENSE file for details.

## References

- [1] [The Hybrid Pseudo Random Number Generator](https://gvpress.com/journals/IJHIT/vol9_no7/27.pdf) by Tanvir Ahmed and Md. Mahbubur Rahman
