from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворення словників у dataclass-об'єкти для зручності
    jobs = [PrintJob(**job) for job in print_jobs]
    printer_constraints = PrinterConstraints(**constraints)
    
    # Сортування завдань: спочатку за пріоритетом (найвищий - 1, найнижчий - 3),
    # потім за часом друку (найкоротший першим)
    # для ефективного групування
    jobs.sort(key=lambda x: (x.priority, x.print_time))

    print_order = []
    total_time = 0
    
    # Використання жадібного підходу для групування завдань
    while jobs:
        current_batch_volume = 0
        current_batch_items = 0
        current_batch_time = 0
        current_batch_ids = []
        
        jobs_to_remove = []

        for job in jobs:
            if (current_batch_volume + job.volume <= printer_constraints.max_volume and
                current_batch_items + 1 <= printer_constraints.max_items):
                
                # Додавання завдання до поточної групи
                current_batch_volume += job.volume
                current_batch_items += 1
                current_batch_time = max(current_batch_time, job.print_time)
                current_batch_ids.append(job.id)
                jobs_to_remove.append(job)
        
        if current_batch_ids:
            # Додавання ідентифікаторів завдань з групи до загального порядку
            print_order.extend(current_batch_ids)
            # Додавання максимального часу друку групи до загального часу
            total_time += current_batch_time
            
            # Видалення оброблених завдань зі списку
            for job in jobs_to_remove:
                jobs.remove(job)

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()