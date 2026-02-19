-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-02-2026 a las 12:39:30
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bookshelf`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `author` varchar(150) NOT NULL,
  `synopsis` text DEFAULT NULL,
  `genre` varchar(80) DEFAULT NULL,
  `year` smallint(6) DEFAULT NULL,
  `cover_color` varchar(20) NOT NULL DEFAULT '#7c6f64',
  `cover_image` varchar(500) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `orden` int(11) DEFAULT 99
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `books`
--

INSERT INTO `books` (`id`, `title`, `author`, `synopsis`, `genre`, `year`, `cover_color`, `cover_image`, `created_by`, `created_at`, `orden`) VALUES
(1, 'El Camino de los Reyes', 'Brandon Sanderson', 'El inicio de la épica saga El Archivo de las Tormentas. En Roshar, un mundo devastado por las Tormentas de Alta, el esclavo Kaladin, la estudiosa Shallan y el soldado Dalinar se ven envueltos en una guerra que podría decidir el destino del mundo.', 'Fantasía', 2010, '#5b4fcf', 'https://covers.openlibrary.org/b/isbn/9780765326355-L.jpg', 1, '2026-02-19 00:35:35', 7),
(2, 'Palabras de Luz', 'Brandon Sanderson', 'Segunda entrega de El Archivo de las Tormentas. Las tramas de Kaladin y Shallan convergen mientras Dalinar intenta unir a los reyes alezi. Los Caballeros Radiantes regresan con poderes que llevan siglos dormidos.', 'Fantasía', 2014, '#7c3aed', 'https://covers.openlibrary.org/b/isbn/9780765326362-L.jpg', 1, '2026-02-19 00:35:35', 9),
(3, 'Juramentada', 'Brandon Sanderson', 'Tercera entrega de El Archivo de las Tormentas. Dalinar afronta su pasado mientras Kaladin lucha con sus juramentos y Shallan se divide entre sus identidades. La Desolación ha llegado.', 'Fantasía', 2017, '#4c1d95', 'https://covers.openlibrary.org/b/isbn/9780765326379-L.jpg', 1, '2026-02-19 00:35:35', 13),
(4, 'Mistborn: El Imperio Final', 'Brandon Sanderson', 'Durante mil años el Lord Legislador ha gobernado un mundo de cenizas y niebla. Una ladrona de élite y su banda de forajidos planean la revolución más imposible de la historia.', 'Fantasía', 2006, '#1e3a5f', 'https://imgs.search.brave.com/GfyHB5b2Pf7VGMlJAueUn-n7oiXaRvsGHhTSYsS_6Uk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9hbHZh/cm9wYXJpcy5jb20v/d3AtY29udGVudC91/cGxvYWRzL0VsLWlt/cGVyaW8tZmluYWwu/anBn', 1, '2026-02-19 00:35:35', 1),
(5, 'El Pozo de la Ascensión', 'Brandon Sanderson', 'Segunda parte de la trilogía Mistborn. Vin y Elend intentan gobernar una ciudad asediada mientras mistborn enemigos y un antiguo mal despiertan en las brumas.', 'Fantasía', 2007, '#1e3a8a', 'https://imgs.search.brave.com/JmS1_yly__odm-TGUZgYESWXaznOLBOQlgdgez49vxY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/cGVuZ3VpbmxpYnJv/cy5jb20vZXMvNzI2/Njk4Ni1sYXJnZV9k/ZWZhdWx0L2VsLXBv/em8tZGUtbGEtYXNj/ZW5zaW9uLWVkaWNp/b24tbGltaXRhZGEt/dHJpbG9naWEtb3Jp/Z2luYWwtbWlzdGJv/cm4tMi53ZWJw', 1, '2026-02-19 00:35:35', 2),
(6, 'El Héroe de las Eras', 'Brandon Sanderson', 'Conclusión de la trilogía Mistborn. Los secretos del Lord Legislador se revelan mientras el mundo se acerca al fin. Vin y Elend afrontan su destino final.', 'Fantasía', 2008, '#172554', 'https://imgs.search.brave.com/UHor672f2nlUd4iAi6flp2ZeQjJidQ5tFScJ9vcP8UI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMuY2RuMi5idXNj/YWxpYnJlLmNvbS9m/aXQtaW4vMzYweDM2/MC80Ni8zNC80NjM0/OWRlNTI5YjY1OGU2/MTRhMzIwNTlmZjBh/MDA1YS5qcGc', 1, '2026-02-19 00:35:35', 3),
(7, 'El Nombre del Viento', 'Patrick Rothfuss', 'La historia de Kvothe, un músico, alquimista y guerrero legendario, contada desde su propio punto de vista en tres días de confesión.', 'Fantasía', 2007, '#7f4f24', 'https://covers.openlibrary.org/b/isbn/9780756404741-L.jpg', 1, '2026-02-19 00:35:35', 4),
(8, 'Cien Años de Soledad', 'Gabriel García Márquez', 'La saga multigeneracional de la familia Buendía en el mítico pueblo de Macondo. Una obra cumbre del realismo mágico y de la literatura universal.', 'Realismo Mágico', 1967, '#b45309', 'https://covers.openlibrary.org/b/isbn/9780060883287-L.jpg', 1, '2026-02-19 00:35:35', 8),
(9, 'La Sombra del Viento', 'Carlos Ruiz Zafón', 'En la Barcelona de la posguerra, un joven descubre un libro que alguien parece querer destruir. El inicio de una búsqueda que revelará oscuros secretos.', 'Misterio', 2001, '#991b1b', 'https://covers.openlibrary.org/b/isbn/9780143034902-L.jpg', 1, '2026-02-19 00:35:35', 5),
(10, 'Don Quijote de la Mancha', 'Miguel de Cervantes', 'El ingenioso hidalgo don Quijote de la Mancha sale al mundo convencido de ser un caballero andante, acompañado de su fiel escudero Sancho Panza.', 'Clásico', 1605, '#065f46', 'https://covers.openlibrary.org/b/isbn/9780060934347-L.jpg', 1, '2026-02-19 00:35:35', 10),
(11, 'El Juego de Ender', 'Orson Scott Card', 'En el futuro, la humanidad entrena a niños genio para combatir a los insectores alienígenas. Ender Wiggin podría ser la última esperanza de la humanidad.', 'Ciencia Ficción', 1985, '#155e75', 'https://covers.openlibrary.org/b/isbn/9780812550702-L.jpg', 1, '2026-02-19 00:35:35', 11),
(12, 'Fundación', 'Isaac Asimov', 'El matemático Hari Seldon prevé la caída del Imperio Galáctico y crea la Fundación para reducir los siglos de barbarie que seguirán.', 'Ciencia Ficción', 1951, '#1e3a5f', 'https://covers.openlibrary.org/b/isbn/9780553293357-L.jpg', 1, '2026-02-19 00:35:35', 12),
(13, 'La Casa de los Espíritus', 'Isabel Allende', 'Cuatro generaciones de mujeres de la familia Trueba en un país latinoamericano ficticio, entrelazando política, amor y magia.', 'Realismo Mágico', 1982, '#7e1d5f', 'https://covers.openlibrary.org/b/isbn/9780553273700-L.jpg', 1, '2026-02-19 00:35:35', 6),
(14, '1984', 'George Orwell', 'En un estado totalitario, Winston Smith trabaja reescribiendo la historia. Su rebelión silenciosa contra el Gran Hermano lo lleva a un destino inevitable.', 'Distopía', 1949, '#374151', 'https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg', 1, '2026-02-19 00:35:35', 14),
(15, 'trenza del mar esmeralda', 'Brandon Sanderson', '', 'Fantasia', 2023, '#7c6f64', 'https://imgs.search.brave.com/iH5Pqdolcj_8DrxrAA-UvqGE5qP020SgAz9tQKSwsJM/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NjE3emdyUlJlbkwu/anBn', 1, '2026-02-19 12:33:29', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(64) NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `is_admin`, `created_at`) VALUES
(1, 'admin', 'admin@bookshelf.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 1, '2026-02-19 00:35:35'),
(2, 'Alex', 'alex@prueba1.com', 'ff960cb55673958c594d0daaab1e368651c75c02f9687192a1811e7b180336a7', 0, '2026-02-19 00:42:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_books`
--

CREATE TABLE `user_books` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `status` enum('quiero_leer','leyendo','leido') NOT NULL DEFAULT 'quiero_leer',
  `rating` tinyint(4) DEFAULT NULL,
  `liked` tinyint(4) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `user_books`
--

INSERT INTO `user_books` (`id`, `user_id`, `book_id`, `status`, `rating`, `liked`, `comment`, `updated_at`) VALUES
(1, 2, 1, 'quiero_leer', 4, 1, NULL, '2026-02-19 00:42:56');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `user_books`
--
ALTER TABLE `user_books`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_user_book` (`user_id`,`book_id`),
  ADD KEY `book_id` (`book_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `user_books`
--
ALTER TABLE `user_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `user_books`
--
ALTER TABLE `user_books`
  ADD CONSTRAINT `user_books_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_books_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
