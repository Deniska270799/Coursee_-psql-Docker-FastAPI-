o
    ��He  �                   @   sV   d dl mZ d dlmZ e� ZejdeeB d�ddefdd��Z	e�
d�d	d
� �ZdS )�    )�FastAPI)�update_currencyz/data)�response_model�totalc                 �   s,   �t �� }|�� }d|d � d|d � d�S )Nu   Курс доллара = �USDu#    рублей.
Курс евро = �EURu    рублей)r   �delay�get)r   �result�sp� r   �#/home/deniska/Desktop/Work1/main.py�get_data	   s   �r   z/update_currencyc                   �   s   �t ��  ddiS )N�messageu=   Задача обновления курса запущена)r   r   r   r   r   r   �run_update_currency_task   s   �r   N)r   )�fastapir   �tasks1r   �appr	   �tuple�str�intr   �postr   r   r   r   r   �<module>   s   	