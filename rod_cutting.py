from typing import List, Dict

def reconstruct_cuts(s: List[int], length: int) -> List[int]:
    """Відновлює список розрізів за допомогою допоміжного масиву `s`."""
    cuts = []
    while length > 0:
        cut = s[length]
        cuts.append(cut)
        length -= cut
    return cuts

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію.

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    memo = {}
    cuts_memo = {}

    def solve(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = -1
        best_cut_length = 0
        
        for i in range(1, n + 1):
            profit = prices[i - 1] + solve(n - i)[0]
            if profit > max_profit:
                max_profit = profit
                best_cut_length = i
        
        memo[n] = (max_profit, best_cut_length)
        return max_profit, best_cut_length

    final_profit, _ = solve(length)
    
    # Реконструкція розрізів
    current_length = length
    cuts = []
    while current_length > 0:
        _, cut_len = memo[current_length]
        cuts.append(cut_len)
        current_length -= cut_len
        
    return {
        "max_profit": final_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if len(cuts) > 0 and cuts[0] != length else 0
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію.

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # dp_profits[i] - максимальний прибуток для стрижня довжини i
    dp_profits = [0] * (length + 1)
    # s[i] - довжина першого відрізка в оптимальному розрізі для довжини i
    s = [0] * (length + 1)
    
    for j in range(1, length + 1):
        max_val = -1
        best_cut = 0
        for i in range(1, j + 1):
            current_profit = prices[i - 1] + dp_profits[j - i]
            if current_profit > max_val:
                max_val = current_profit
                best_cut = i
        dp_profits[j] = max_val
        s[j] = best_cut
    
    final_profit = dp_profits[length]
    cuts = reconstruct_cuts(s, length)

    return {
        "max_profit": final_profit,
        "cuts": sorted(cuts), # Сортуємо для узгодженості
        "number_of_cuts": len(cuts) - 1 if len(cuts) > 0 and sum(cuts) == length and len(cuts)>1 else 0
    }

def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()