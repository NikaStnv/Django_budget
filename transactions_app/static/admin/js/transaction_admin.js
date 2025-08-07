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
                cell.closest('tr').style.backgroundColor = '#e6f7e6';
            } 
            else if (text === 'Витрата') {
                // Підсвічуємо всю строку зеленим
                cell.closest('tr').style.backgroundColor = '#ffebee';
            }
        });
    });
})();