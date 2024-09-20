class RepairCalculator:
    def calculate_repair_cost(self, part_cost, labor_cost, additional_fees):
        """
        Рассчитывает общую стоимость ремонта.
        
        :param part_cost: Стоимость деталей
        :param labor_cost: Стоимость работы
        :param additional_fees: Дополнительные сборы
        :return: Общая стоимость ремонта
        """
        return part_cost + labor_cost + additional_fees

    def calculate_repair_time(self, hours, minutes):
        """
        Рассчитывает общее время ремонта в формате часов и минут.
        """
        return hours, minutes

    def calculate_discounted_cost(self, total_cost, discount_percentage):
        """
        Рассчитывает стоимость с учетом скидки.
    
        :param total_cost: Общая стоимость
        :param discount_percentage: Процент скидки
        :return: Итоговая стоимость
        """
        return total_cost - (total_cost * discount_percentage / 100)

