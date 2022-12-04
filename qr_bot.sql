-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Дек 04 2022 г., 18:44
-- Версия сервера: 10.4.24-MariaDB
-- Версия PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `qr_bot`
--

-- --------------------------------------------------------

--
-- Структура таблицы `messages`
--

CREATE TABLE `messages` (
  `primary_id` int(10) NOT NULL,
  `msg_id` varchar(200) NOT NULL,
  `file_id` varchar(200) NOT NULL,
  `user_id` int(20) NOT NULL,
  `chat_id` int(20) NOT NULL,
  `proove_file` varchar(200) DEFAULT NULL,
  `proove_desc` varchar(300) NOT NULL,
  `proved` int(1) NOT NULL DEFAULT 0,
  `time` datetime NOT NULL DEFAULT current_timestamp(),
  `rejected` int(1) NOT NULL,
  `prod_id` int(20) NOT NULL,
  `file_type` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `messages`
--

INSERT INTO `messages` (`primary_id`, `msg_id`, `file_id`, `user_id`, `chat_id`, `proove_file`, `proove_desc`, `proved`, `time`, `rejected`, `prod_id`, `file_type`) VALUES
(62, '7427', 'AQADbcUxGyQ-aEh9.jpg', 380844272, 380844272, 'AQADosQxGyQ-aEh-.jpg', 'Tariflimiz', 2, '2022-12-04 22:40:03', 0, 13, 'image/jpeg');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(20) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `lang` varchar(2) NOT NULL,
  `is_admin` int(1) NOT NULL,
  `tel` varchar(14) NOT NULL,
  `status` int(2) NOT NULL,
  `msg_id` int(20) NOT NULL,
  `chat_id` int(20) NOT NULL,
  `seller_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `full_name`, `lang`, `is_admin`, `tel`, `status`, `msg_id`, `chat_id`, `seller_id`) VALUES
(380844272, 'Lazizjonov Jasurbek', 'uz', 1, '998946380341', 0, 7427, 380844272, 53);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`primary_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `messages`
--
ALTER TABLE `messages`
  MODIFY `primary_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
