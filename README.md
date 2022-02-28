# Demo

![caption](https://github.com/xx-CRAZINESS-xx/Ecommerce/blob/main/Video/market.gif)


# Run Locally

#### Create an environment

```
conda create -n flask_app python=3.7 -y
```

#### Activate the environment

```
conda activate flask_app
```

#### Install the requirements

```
pip install -r requirements.txt
```
# Additional commands

#### To create a new product or user through terminal
```
python
from market import db
from market import Item
db.create_all()
item1=Item(name=" ",price=,barcode=" ",description=" ")
user1=User(user_name=" ",email_address=" ",password=" ")

db.session.add(item1)
db.session.add(user1)
db.session.commit()
Item.query.all()
User.query.all()
```

#### To filter a product/user through terminal

```
item1=Item.query.filter_by(name='IPhone 13 Pro Max').first()
item1.owner=User.query.filter_by(user_name=' ').first()
```

#### To get the secret key through terminal
```
python
import os
os.urandom(12).hex()
```
