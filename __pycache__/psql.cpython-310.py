o
    ��He�  �                	   @   s�   d dl mZmZmZmZmZmZmZ d dlm	Z	 d dl
mZ dZee�Ze	dded�Ze� Ze� Zedeeded	d	d
�ede�ede��ZG dd� de�Zejjed� dd� ZdS )�    )�create_engine�Column�Float�Integer�MetaData�Table�Text)�sessionmaker)�declarative_basez+postgresql://postgres:527619@localhost/TestF)�
autocommit�	autoflush�bind�currency_rates�idT)�primary_key�index�usd_rate�eur_ratec                   @   s   e Zd ZeZdS )�CurrencyRatesN)�__name__�
__module__�__qualname__r   �	__table__� r   r   �#/home/deniska/Desktop/Work1/psql.pyr      s    r   )r   c                 C   sJ   t � �}t| |d�}|�|� |��  W d   � d S 1 sw   Y  d S )N)r   r   )�SessionLocalr   �add�commit)r   r   �session�db_currency_ratesr   r   r   �save_currency_rates   s
   

"�r    N)�
sqlalchemyr   r   r   r   r   r   r   �sqlalchemy.ormr	   �sqlalchemy.ext.declarativer
   �DATABASE_URL�enginer   �Base�metadatar   r   �
create_allr    r   r   r   r   �<module>   s$   $ �