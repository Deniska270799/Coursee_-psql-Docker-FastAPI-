o
    >�HeU  �                   @   sL   d dl mZ d dlmZ d dlZe� ZejdeeB d�d	de	fdd��Z
dS )
�    )�FastAPI)�BeautifulSoupNz/data)�response_model�totalc                 �   s�   �d}d d d�}|D ]C}t �|�}t|jd�}|�dd�}|dkr)t|j�|d< q
t|j�|d< td	|d � d
|d � d�� d	|d � d
|d � d�  S d S )N)�&https://ru.myfin.by/currency/cb-rf/usdz&https://ru.myfin.by/currency/cb-rf/eur)�USD�EURzhtml.parser�p�h1r   r   r   u   Курс доллара = u#    рублей.
Курс евро = u    рублей)�requests�getr   �text�find�float�print)r   �urls�sp�url�response�data�value� r   �#/home/deniska/Desktop/Work1/Work.py�get_data   s   �

�r   )r   )�fastapir   �bs4r   r   �appr   �tuple�str�intr   r   r   r   r   �<module>   s    