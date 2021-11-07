class Menu:
    def __init__(self):
        self.items = {
            'Latte': {
                'water': 100,
                'coffee': 50,
                'milk': 100,
                'cost': 10
            }, 'Cappuccino': {
                'water': 150,
                'coffee': 50,
                'milk': 150,
                'cost': 10
            }, 'Espresso': {
                'water': 120,
                'coffee': 60,
                'milk': 130,
                'cost': 10
            }, 'coffee_making_charge': 10}

    def get_items(self):
        return self.items


class Coffee:
    def __init__(self):
        self.total_resources = {
            'water': 500,
            'coffee': 500,
            'milk': 500,
            'total_coins': 500
        }
        self.standard_cost_of_resources = {
            'water': {'500ml': 10},
            'coffee': {'500g': 20},
            'milk': {'500ml': 30}
        }

    def get_total_resources(self):
        return self.total_resources

    def get_standard_cost_of_resources(self):
        return self.standard_cost_of_resources

    def is_resource_sufficient(self, user_coffee_choice):
        try:
            items = Menu().get_items()
            user_choice_item = items[user_coffee_choice]
            if user_choice_item['water'] <= self.total_resources['water'] and \
                    user_choice_item['coffee'] <= self.total_resources['coffee'] and \
                    user_choice_item['milk'] <= self.total_resources['milk']:
                return {'status': 200, "is_resource_sufficient": True}
            else:
                return {'status': 500, "is_resource_sufficient": False}
        except Exception as e:
            return {'status': 500, 'error': e}

    def make_coffee(self, user_choice):
        try:
            items = Menu().get_items()
            print(user_choice, items[user_choice])
            total_resources = self.get_total_resources()
            total_resources['water'] -= items[user_choice]['water']
            total_resources['coffee'] -= items[user_choice]['coffee']
            total_resources['milk'] -= items[user_choice]['milk']
            total_resources['total_coins'] -= items[user_choice]['cost'] + items['coffee_making_charge']
            return {'status': 200, "total_resources:": total_resources}
        except Exception as e:
            return {'status': 500, 'error': e}


class Payment:
    def __init__(self):
        pass

    def add_coins(self, coins_entered_by_user):
        try:
            total_resources = Coffee().get_total_resources()
            total_resources['total_coins'] += coins_entered_by_user
            return {'status': 200, 'total_coins_left:': total_resources['total_coins']}
        except Exception as e:
            return {'status': 500, 'error': e}

    def add_resources(self, water, coffee, milk):
        try:
            total_resources = Coffee().get_total_resources()
            total_resources['water'] += water
            total_resources['coffee'] += coffee
            total_resources['milk'] += milk
            return {'status': 200, 'total_resources_left:': total_resources}
        except Exception as e:
            return {'status': 500, 'error': e}

    def make_payment(self, payment_by_user):
        try:
            total_resources = Coffee().get_total_resources()
            total_resources['total_coins'] -= payment_by_user
            return {'status': 200, 'total_coins_left:': total_resources['total_coins']}
        except Exception as e:
            return {'status': 500, 'error': e}
