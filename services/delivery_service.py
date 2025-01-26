def calculate_delivery(base_price: int, selected_range: dict[str, int], order_minimum_no_surcharge: int, distance: int, cart_value: int) -> tuple[int, int, int]:
        """
        Calculating delivery related charges according to distance and minimum order surcharges

        Args:
            base_price (int): base price of delivery fee
            selected_range (dict): the selected range for a and b parameters of formula given based on distance
            distance (int): distance between venue and user
            order_minimum_no_surcharge (int): lowest orderable price of the venue
            cart_value (int): order price

        Returns: 
            tuple[int, int, int]: delivery fee, surcharge for under minumum order amount, summary of all delivery related charges
        """

        #calculating delivery fee
        delivery_fee = int(base_price + selected_range["a"] + round(selected_range["b"] * distance / 10))
        
        #calculating small order surcharge
        small_order_surcharge = int(max(0, round(order_minimum_no_surcharge-cart_value)))
        
        #calculating total price
        total_price = round(cart_value) + delivery_fee + small_order_surcharge
        
        return delivery_fee, small_order_surcharge, total_price