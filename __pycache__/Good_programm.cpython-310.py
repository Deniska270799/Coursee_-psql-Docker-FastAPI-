o
    v�Hez
  �                	   @   s�   d dl mZ d dlmZ d dlZd dlmZmZmZm	Z	m
Z
mZ d dlmZ d dlmZ e� ZdZee�Zedded	�Ze� Ze
� Zed
eede	ddd�ede�ede��Zejedd� G dd� de�Zdd� Zejded�dd� �ZdS )�    )�FastAPI)�BeautifulSoupN)�create_engine�Column�Float�Integer�MetaData�Table)�sessionmaker)�declarative_basez+postgresql://postgres:527619@localhost/TestF)�
autocommit�	autoflush�bind�currency_rates�idT)�primary_key�index�usd_rate�eur_rate)�
checkfirstc                   @   s   e Zd ZeZdS )�CurrencyRatesN)�__name__�
__module__�__qualname__r   �	__table__� r   r   �,/home/deniska/Desktop/Work1/Good_programm.pyr   2   s    r   c                  �   sf   �d} d d d�}| D ]&}t �|�}t|jd�}|�dd�}|dkr)t|j�|d< q
t|j�|d< q
|S )	N)�&https://ru.myfin.by/currency/cb-rf/usdz&https://ru.myfin.by/currency/cb-rf/eur)�USD�EURzhtml.parser�p�h1r   r   r   )�requests�getr   �text�find�float)�urls�sp�url�response�data�valuer   r   r   �get_currency_rates6   s   �

r-   z/data)�response_modelc                  �   s`   �t � I d H } t� �}t| d | d d�}|�|� |��  W d   � | S 1 s)w   Y  | S )Nr   r   )r   r   )r-   �SessionLocalr   �add�commit)r   �session�db_currency_ratesr   r   r   �get_dataD   s   �


��r4   )�fastapir   �bs4r   r"   �
sqlalchemyr   r   r   r   r   r	   �sqlalchemy.ormr
   �sqlalchemy.ext.declarativer   �app�DATABASE_URL�enginer/   �Base�metadatar   �creater   r-   r#   �dictr4   r   r   r   r   �<module>   s0    �	