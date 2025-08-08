// super-simple-colorize.js
(function() {
    // 1. Чекаємо завантаження сторінки
    document.addEventListener('DOMContentLoaded', function() {
        // 2. Знаходим усі ячейки таблиці
        const allCells = document.querySelectorAll('td');
        
        // 3. Шукаємо ячейки з текстом "Дохід" или "Витрата"
        allCells.forEach(cell => {
            const text = cell.textContent.trim();
            
            if (text === 'Дохід') {
                // Підсвічуємо всю строку зеленим
                cell.closest('tr').style.backgroundColor = '#50b4b4ff';
            } 
            else if (text === 'Витрата') {
                // Підсвічуємо всю строку зеленим
                cell.closest('tr').style.backgroundColor = '#a54754ff';
            }
        });
    });
})();