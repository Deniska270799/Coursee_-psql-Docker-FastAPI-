o
    w�He�  �                   @   s:   d dl mZ d dlmZ d dlZed�Zejdd� �ZdS )�    )�Celery)�BeautifulSoupN�currency_updatec                  C   s�   d} d d d�}| D ]&}t �|�}t|jd�}|�dd�}|dkr(t|j�|d< q	t|j�|d< q	td	|d � d
|d � d�� |S )N)�&https://ru.myfin.by/currency/cb-rf/usdz&https://ru.myfin.by/currency/cb-rf/eur)�USD�EURzhtml.parser�p�h1r   r   r   u   Курс доллара = u#    рублей.
Курс евро = u    рублей)�requests�getr   �text�find�float�print)�urls�sp�url�response�data�value� r   �%/home/deniska/Desktop/Work1/tasks1.py�update_currency	   s   

r   )�celeryr   �bs4r   r
   �app�taskr   r   r   r   r   �<module>   s   