from sqlmodel import Session, select, update
from app import engine

from app.models.products import Product
from app.models.orders import OrderCreate, OrderLineItemStub, Order
from app.models.order_line_items import OrderLineItem, OrderLineItemCreate

class OrderService:

    @classmethod
    def create_order(cls, order_request: OrderCreate):
        with Session(engine) as session:
            order_data = order_request.model_dump(exclude_unset=True)
            new_order = Order.model_validate(order_data)

            session.add(new_order)
            session.flush()

            #Create/add any order_line_items if they exist
            if order_request.line_items and len(order_request.line_items):
                for line_item in order_request.line_items:
                    product = session.get(Product, line_item["product_id"]) # There should only be one match according to id

                    #Create the line item if ID matches
                    if (product):
                        new_line = OrderLineItemCreate(product_id=line_item["product_id"],
                                                       product_name=product.name,
                                                       product_price=product.price,
                                                       product_qty=line_item["quantity"],
                                                       order_id=new_order.order_id_pk,
                                                       stock_quantity=0, #Uknown column purpose? TODO: VERIFY COLUMN PURPOSE
                                                       line_type_id=0)

                        line_data = new_line.model_dump()
                        valid_product = OrderLineItem.model_validate(line_data)

                        session.add(valid_product)

            #Commit everything to the database
            session.commit()
            session.refresh(new_order)

        return new_order

