o
    ��He`  �                   @   sL   d dl mZ d dlZd dlmZ d dlmZ e� Zejde	d�dd� �Z
dS )	�    )�FastAPIN)�BeautifulSoup)�save_currency_ratesz/data)�response_modelc                  �   sx   �d} d d d�}| D ]&}t �|�}t|jd�}|�dd�}|dkr)t|j�|d< q
t|j�|d< q
t|d |d � |S )	N)�&https://ru.myfin.by/currency/cb-rf/usdz&https://ru.myfin.by/currency/cb-rf/eur)�USD�EURzhtml.parser�p�h1r   r   r   )�requests�getr   �text�find�floatr   )�urls�currency_rates�url�response�data�value� r   �&/home/deniska/Desktop/Work1/FastAPI.py�get_data   s   �

r   )�fastapir   r   �bs4r   �psqlr   �appr   �dictr   r   r   r   r   �<module>   s    