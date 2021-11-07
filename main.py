from coffee import Menu, Coffee, Payment

menu = Menu()
coffee = Coffee()
payment = Payment()


def main():
    try:
        is_machine_on = True

        while is_machine_on:
            user_name = input('Enter your name:')
            print(f'Hello {user_name}, Help us offer you the best coffee \n Check our menu below \n')
            get_items = menu.get_items()
            print(get_items)
            user_coffee_choice = input('Choose your favourite coffee, from the list:')
            while user_coffee_choice not in get_items.keys():
                user_coffee_choice = input('Please make sure the coffee is in the list or check your spelling:')

            # check if the resources against the coffee is enough
            is_resource_enough = coffee.is_resource_sufficient(user_coffee_choice)
            if is_resource_enough['status'] == 200:
                coffee_cost = menu.get_items()[user_coffee_choice]['cost'] + menu.get_items()['coffee_making_charge']

                # Check if there are enough coins for making payment
                total_coins_left = coffee.get_total_resources()['total_coins']
                if coffee_cost <= total_coins_left:
                    make_payment = payment.make_payment(coffee_cost)
                    if make_payment['status'] == 200:
                        make_coffee = coffee.make_coffee(user_coffee_choice)
                        if make_coffee['status'] == 200:
                            print('YOUR COFFEE IS READY')
                            is_machine_on = False
                            break

                else:  # if there are not enough coins
                    print(f'There is not enough coins left: {total_coins_left}, minimum amount to add is {coffee_cost}')
                    input_user_coins = int(input('Enter the coins you want to add:'))
                    while input_user_coins < coffee_cost:
                        input_user_coins = int(input(f'You need to add a minimum of {coffee_cost}:'))
                    add_coins = payment.add_coins(input_user_coins)
                    if add_coins['status'] == 200:
                        make_payment = payment.make_payment(coffee_cost)
                        if make_payment['status'] == 200:
                            make_coffee = coffee.make_coffee(user_coffee_choice)
                            if make_coffee['status'] == 200:
                                print('YOUR COFFEE IS READY')
                                is_machine_on = False
                                break

            else:  # if resources are not enough
                print(f'You do not have enough resources left, check this {coffee.get_total_resources()}')
                print('choose the options for adding resources\n '
                      'water(ml): 1.) 1000 2.)500 3.)300 \n'
                      'Coffee(g): 1.) 1000 2.)500 3.)300 \n'
                      'milk(ml): 1.) 1000 2.)500 3.)300 \n')

                add_water = int(input('choose the quantity for water, choose  1500, 1000, 500'))
                while add_water not in [1500, 1000, 500]:
                    print('Recheck your input')
                    add_water = int(input('choose the quantity for water, press 1500, 1000, 500: '))

                add_coffee = int(input('choose the quantity for coffee, press 1500, 1000, 50000'))
                while add_coffee not in [1500, 1000, 500]:
                    print('Recheck your input')
                    add_coffee = int(input('choose the quantity for coffee, press  1500, 1000, 500: '))

                add_milk = int(input('choose the quantity for milk, press 1500, 1000, 500'))
                while add_milk not in [1500, 1000, 500]:
                    print('Recheck your input')
                    add_milk = int(input('choose the quantity for coffee, choose 1500, 1000, 500: '))

                # calculate the total cost of resources entered by users
                std_cost_resources = coffee.get_standard_cost_of_resources()
                water = (add_water * std_cost_resources['water']['500ml']) // 500
                coffeee = (add_coffee * std_cost_resources['coffee']['500g']) // 500
                milk = (add_milk * std_cost_resources['milk']['500ml']) // 500

                total_cost_of_resources = water + milk + coffeee
                # check if enough coins
                total_coins_left = coffee.get_total_resources()['total_coins']

                if total_cost_of_resources < total_coins_left:
                    # make payment
                    make_payment = payment.make_payment(total_cost_of_resources)
                    if make_payment['status'] == 200:
                        # add resources
                        add_resources = payment.add_resources(water, coffeee, milk)
                        if add_resources['status'] == 200:
                            make_coffee = coffee.make_coffee(user_coffee_choice)
                            if make_coffee['status'] == 200:
                                print('YOUR COFFEE IS READY')
                                is_machine_on = False
                                break

                else:  # not enough coin
                    print('You do not have enough coins')
                    user_choice_to_add_coins = input(f'Add {total_cost_of_resources} to buy coffee?: Y or N?')

                    while user_choice_to_add_coins not in ['y', 'n', 'Y', 'N']:
                        user_choice_to_add_coins = input('please press: Y or N?')

                    if user_choice_to_add_coins in ['Y', 'y']:
                        add_coins = payment.add_coins(total_cost_of_resources)

                        if add_coins['status'] == 200:
                            make_payment = payment.make_payment(total_cost_of_resources)
                            if make_payment['status'] == 200:
                                make_coffee = coffee.make_coffee(user_coffee_choice)
                                if make_coffee['status'] == 200:
                                    print('YOUR COFFEE IS READY')
                                    is_machine_on = False
                                    break
                    else:
                        break

    except Exception as e:
        return e


main()