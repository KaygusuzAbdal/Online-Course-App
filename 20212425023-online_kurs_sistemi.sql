-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 25 Ara 2022, 16:19:52
-- Sunucu sürümü: 10.4.27-MariaDB
-- PHP Sürümü: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `online_kurs_sistemi`
--

DELIMITER $$
--
-- Yordamlar
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `admin_listesi` ()   SELECT users.user_id, CONCAT(users.name," ",users.surname) AS full_name, users.phone, users.email, users.cash, roles.role_id, roles.name AS role
FROM users, user_roles, roles
WHERE users.user_id = user_roles.user_id
AND roles.role_id = user_roles.role_id
GROUP BY users.user_id HAVING roles.role_id < 3$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `adresi_olmayan_kullanicilar` ()   SELECT users.user_id, CONCAT(users.name, " ",users.surname) AS kullanici, users.phone AS tel_no, users.email
FROM users, roles, user_roles
WHERE users.user_id NOT IN (SELECT addresses.user_id FROM addresses)
AND roles.name LIKE "%user%"
AND user_roles.role_id = roles.role_id
AND user_roles.user_id = users.user_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `bos_kategoriler` ()   SELECT categories.name AS kurs_eklenmemis_kategoriler
FROM categories
WHERE categories.name
NOT IN (
    SELECT categories.name 
    FROM courses, categories, course_categories 
    WHERE courses.course_id = course_categories.course_id
    AND course_categories.category_id = categories.category_id
	)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `egitmenin_fiyat_ortalamasi` (IN `egitmen_adi` VARCHAR(100))   SELECT users.name AS egitmen, ROUND(AVG(courses.price),2) AS kurslarinin_fiyat_ortalamasi
FROM users, courses
WHERE users.user_id = courses.instructor_id
AND (
	(users.name LIKE CONCAT("%",egitmen_adi,"%"))
    OR
    (users.surname LIKE CONCAT("%",egitmen_adi,"%"))
	)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `egitmenin_kurslari` (IN `egitmen_adi` VARCHAR(100))   SELECT CONCAT(users.name," ",users.surname) AS egitmen, courses.name
FROM users, courses, roles, user_roles
WHERE roles.name LIKE "%instructor%" 
AND user_roles.role_id = roles.role_id
AND user_roles.user_id = users.user_id
AND (
    (users.name LIKE CONCAT("%",egitmen_adi,"%"))
    OR 
    (users.surname LIKE CONCAT("%",egitmen_adi,"%")))
AND users.user_id = courses.instructor_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `en_populer_kurs` ()   SELECT courses.name AS course, categories.name AS category, COUNT(users.user_id) AS students, courses.price, courses.description
FROM categories, courses, course_categories, users,
user_courses
WHERE courses.course_id = course_categories.course_id
AND course_categories.category_id = categories.category_id
AND user_courses.course_id = courses.course_id
AND user_courses.user_id = users.user_id
GROUP BY users.user_id ORDER BY students
DESC LIMIT 1$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `fiyat_filtrelemesi` (IN `minimum_fiyat` INT, IN `maximum_fiyat` INT)   SELECT courses.name, categories.name AS category, CONCAT(users.name, " ",users.surname) AS instructor, courses.price, courses.description
FROM courses, users, categories, course_categories
WHERE courses.price BETWEEN minimum_fiyat AND maximum_fiyat
AND courses.instructor_id = users.user_id
AND courses.course_id = course_categories.course_id
AND course_categories.category_id = categories.category_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `kategorideki_kurslar` (IN `kategori` VARCHAR(255))   SELECT categories.name AS category, courses.name AS course, CONCAT(users.name," ",users.surname) AS instructor, courses.price, courses.description
FROM categories, courses, course_categories, users
WHERE course_categories.course_id = courses.course_id
AND course_categories.category_id = categories.category_id
AND categories.name LIKE CONCAT("%",kategori,"%")
AND users.user_id = courses.instructor_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `kategorideki_kurs_sayisi` (IN `category_id` INT)   SELECT categories.name AS kategori, COUNT(courses.course_id) AS kategoride_bulunan_toplam_kurs_sayisi
FROM categories, courses, course_categories
WHERE course_categories.course_id = courses.course_id
AND course_categories.category_id = categories.category_id
AND categories.category_id = category_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `kullanicilarin_kurslari` ()  NO SQL SELECT CONCAT(users.name," ",users.surname) AS kullanici, courses.name AS kurs FROM users, courses, user_courses
WHERE users.user_id = user_courses.user_id
AND user_courses.course_id = courses.course_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `kullanicinin_adresleri` (IN `kullanici` VARCHAR(100))   SELECT CONCAT(users.name, " ",users.surname) AS full_name, addresses.name, addresses.country, addresses.city, addresses.description
FROM users, addresses
WHERE users.user_id = addresses.user_id
AND (
    (users.name LIKE CONCAT("%",kullanici,"%"))
    OR
    (users.surname LIKE CONCAT("%",kullanici,"%"))
	)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `kurslari_getir` ()  NO SQL SELECT courses.name AS kurs, CONCAT(users.name," ",users.surname) AS egitmen, categories.name AS kategori, courses.price AS fiyat, courses.description AS aciklama
FROM courses, categories, course_categories, users
WHERE courses.course_id = course_categories.course_id
AND course_categories.category_id = categories.category_id
AND courses.instructor_id = users.user_id GROUP BY kurs ORDER BY kurs ASC$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `addresses`
--

CREATE TABLE `addresses` (
  `address_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `addresses`
--

INSERT INTO `addresses` (`address_id`, `user_id`, `name`, `country`, `city`, `description`) VALUES
(1, 1, 'ev', 'Türkiye', 'Manisa', 'Yunusemre 1503 Sokak'),
(2, 1, 'eski ev', 'Türkiye', 'İzmir', 'Mansuroğlu Mah.'),
(3, 2, 'okul', 'Türkiye', 'İzmir', 'Balçova, İzmir Ekonomi Üniversitesi'),
(4, 3, 'ev', 'Türkiye', 'İzmir', 'Poligon, 1307 Sokak'),
(5, 4, 'deneme', 'Türkiye', 'Antalya', ''),
(6, 5, 'universite', 'Türkiye', 'Manisa', 'Celal Bayar Üniversitesi'),
(7, 6, 'ev', 'Türkiye', 'Manisa', 'Yunusemre 1503 Sokak'),
(8, 7, 'iş', 'Türkiye', 'Antalya', 'Alanya'),
(9, 8, 'ev', 'Türkiye', 'İstanbul', 'Taksim'),
(10, 9, 'asddafs', 'Türkiye', 'Ankara', '');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `categories`
--

INSERT INTO `categories` (`category_id`, `name`) VALUES
(1, 'Yazılım Geliştirme'),
(2, 'Kişisel Gelişim'),
(3, 'Tasarım'),
(4, 'Fotoğraf ve Video'),
(5, 'Sağlık ve Fitness'),
(6, 'Müzik'),
(7, 'Sınava Hazırlık'),
(8, 'Dil Öğrenimi'),
(9, 'El Sanatları'),
(10, 'Evcil Hayvan Bakımı');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `courses`
--

CREATE TABLE `courses` (
  `course_id` int(11) NOT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `price` decimal(18,0) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `courses`
--

INSERT INTO `courses` (`course_id`, `instructor_id`, `name`, `price`, `description`) VALUES
(1, 4, 'Adım Adım Matematik', '34', 'Uygulamalarla adım adım matematik'),
(2, 5, 'Köpek Eğitimi', '32', 'En saldırgan köpekleri bile dize getirebileceksiniz'),
(3, 6, 'Premiere Pro ile Video Editleme', '40', 'Premiere Pro CC uygulamasını kullanabileceksiniz'),
(4, 4, 'İngilizce Kursu', '50', 'Ana Dilin Gibi İngilizce Konuş!!'),
(5, 5, 'Sıfırdan İleri Seviyeye Fransızca', '19', 'Gözünde büyüttüğün kadar zor değil'),
(6, 4, 'TOEFL Kursu', '25', 'O sene bu sene! Bu kurs sayesinde artık TOEFL sınavı cepte!'),
(7, 5, 'Seslendirme Sanatçılığı', '23', 'Ses sanatçısı olun'),
(8, 6, 'Veri Tabanı Sistemleri', '40', 'SQL ile işlemler yapmayı öğrenin'),
(9, 4, 'Web Geliştirme', '50', 'Kendi web sitenizi yaratmayı öğrenip, sektörde aranan kişi olacaksınız!'),
(10, 4, 'Fotoğrafçılık Kursu', '45', 'Bu kurs ile bakış açınızı değiştireceksiniz'),
(11, 6, 'Girişimcilik Kursu', '55', 'Risk almaktan korkma!');

--
-- Tetikleyiciler `courses`
--
DELIMITER $$
CREATE TRIGGER `kurs_eklendiginde_log` AFTER INSERT ON `courses` FOR EACH ROW INSERT INTO log_records(description, actualized_by, actualized_at) VALUES (
    CONCAT(new.name," isimli kurs eklendi. ID: ",new.course_id," - InstructorID: ",new.instructor_id)
    ,NULL,Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_eklendiginde_ortalama` AFTER INSERT ON `courses` FOR EACH ROW INSERT INTO price_average_of_courses(price_average, last_checked_at)
VALUES ((SELECT AVG(courses.price) FROM courses), Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_eklendiginde_sayi` AFTER INSERT ON `courses` FOR EACH ROW INSERT INTO total_courses(total_course_count, last_checked_at)
VALUES ((SELECT COUNT(*) FROM courses), Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_guncellendiginde_log` BEFORE UPDATE ON `courses` FOR EACH ROW INSERT INTO log_records(description, actualized_by, actualized_at) VALUES (
    CONCAT(new.name," isimli kurs güncellendi. ID: ",new.course_id," - InstructorID: ",new.instructor_id)
    ,NULL,Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_guncellendiginde_ortalama` AFTER UPDATE ON `courses` FOR EACH ROW INSERT INTO price_average_of_courses(price_average, last_checked_at)
VALUES ((SELECT AVG(courses.price) FROM courses), Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_silindiginde_kaydet` AFTER DELETE ON `courses` FOR EACH ROW INSERT INTO deleted_courses(course_id, instructor_id, name, price, description) VALUES (old.course_id, old.instructor_id, old.name, old.price, old.description)
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_silindiginde_log` AFTER DELETE ON `courses` FOR EACH ROW INSERT INTO log_records(description, actualized_by, actualized_at) VALUES (CONCAT(old.name," isimli kurs silindi. ID: ",old.course_id," - InstructorID", old.instructor_id),NULL,Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_silindiginde_ortalama` AFTER DELETE ON `courses` FOR EACH ROW INSERT INTO price_average_of_courses(price_average, last_checked_at)
VALUES ((SELECT AVG(courses.price) FROM courses), Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kurs_silindiginde_sayi` AFTER DELETE ON `courses` FOR EACH ROW INSERT INTO total_courses(total_course_count, last_checked_at)
VALUES ((SELECT COUNT(*) FROM courses), Now())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `course_categories`
--

CREATE TABLE `course_categories` (
  `id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `course_categories`
--

INSERT INTO `course_categories` (`id`, `course_id`, `category_id`) VALUES
(1, 1, 7),
(2, 2, 10),
(3, 3, 3),
(4, 3, 4),
(5, 4, 7),
(6, 4, 8),
(7, 5, 7),
(8, 5, 8),
(9, 6, 7),
(10, 7, 6),
(11, 8, 1),
(12, 9, 1),
(13, 10, 4),
(14, 11, 2);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `deleted_courses`
--

CREATE TABLE `deleted_courses` (
  `course_id` int(11) NOT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `price` decimal(18,2) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `deleted_courses`
--

INSERT INTO `deleted_courses` (`course_id`, `instructor_id`, `name`, `price`, `description`) VALUES
(15, 6, 'deneme', '17.00', 'deneme icin olusturdum'),
(23, 4, 'test2 kursu', '190.00', '2. test kursu'),
(32, 4, 'photoshop kursu', '62.00', 'sertifikalı photoshop kursu');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `log_records`
--

CREATE TABLE `log_records` (
  `log_id` int(11) NOT NULL,
  `description` varchar(255) NOT NULL,
  `actualized_by` int(11) DEFAULT NULL,
  `actualized_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `log_records`
--

INSERT INTO `log_records` (`log_id`, `description`, `actualized_by`, `actualized_at`) VALUES
(4, 'deneme isimli kurs eklendi. ID: 15 - InstructorID: 6', NULL, '2022-12-25 02:31:56'),
(5, 'deneme isimli kurs silindi. ID: 15 - InstructorID6', NULL, '2022-12-25 02:31:39'),
(6, 'zeki can gözcu isimli kullanıcının bilgileri değiştirildi. ID: 10', NULL, '2022-12-25 02:34:06'),
(7, 'test2 kursu isimli kurs eklendi. ID: 23 - InstructorID: 4', NULL, '2022-12-25 02:53:20'),
(8, 'test2 kursu isimli kurs silindi. ID: 23 - InstructorID4', NULL, '2022-12-25 02:57:20'),
(9, 'photoshop kursu isimli kurs eklendi. ID: 52 - InstructorID: 4', NULL, '2022-12-25 02:59:41'),
(10, 'photoshop kursu isimli kurs güncellendi. ID: 32 - InstructorID: 4', NULL, '2022-12-25 03:01:47'),
(11, 'photoshop kursu isimli kurs güncellendi. ID: 32 - InstructorID: 4', NULL, '2022-12-25 03:02:33'),
(12, 'photoshop kursu isimli kurs silindi. ID: 32 - InstructorID4', NULL, '2022-12-25 03:02:41');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `price_average_of_courses`
--

CREATE TABLE `price_average_of_courses` (
  `id` int(11) NOT NULL,
  `price_average` int(11) NOT NULL,
  `last_checked_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `price_average_of_courses`
--

INSERT INTO `price_average_of_courses` (`id`, `price_average`, `last_checked_at`) VALUES
(1, 54, '2022-12-25 03:01:47'),
(2, 40, '2022-12-25 03:02:33'),
(3, 38, '2022-12-25 03:02:41');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `roles`
--

CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `roles`
--

INSERT INTO `roles` (`role_id`, `name`) VALUES
(1, 'owner'),
(2, 'admin'),
(3, 'instructor'),
(4, 'user');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `total_courses`
--

CREATE TABLE `total_courses` (
  `id` int(11) NOT NULL,
  `total_course_count` int(11) NOT NULL,
  `last_checked_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `total_courses`
--

INSERT INTO `total_courses` (`id`, `total_course_count`, `last_checked_at`) VALUES
(4, 11, '2022-12-25 02:57:20'),
(6, 12, '2022-12-25 02:59:41'),
(7, 11, '2022-12-25 03:02:41');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `pword` varchar(255) NOT NULL,
  `cash` decimal(18,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`user_id`, `name`, `surname`, `phone`, `email`, `pword`, `cash`) VALUES
(1, 'mustafa cüneyt', 'kafes', '05309050790', 'm.cuneytkafes@gmail.com', '123asd', '100.00'),
(2, 'ahmet ali', 'yılmaz', '05324139007', 'a.yilmaz@gmail.com', '123asd', '2.00'),
(3, 'fatma', 'karabulut', '05321050500', 'f.karabulut@gmail.com', '123asd', '500.00'),
(4, 'kemal', 'karaca', '05302208970', 'k.karaca@gmail.com', '123asd', '70.00'),
(5, 'celal', 'korkmaz', '05327771354', 'celal.korkmaz@gmail.com', '123asd', '50.00'),
(6, 'defne deniz', 'aksoy', '05553280019', 'defne.aksoy@gmail.com', '123asd', '40.00'),
(7, 'berkay', 'karakuş', '05527203941', 'b.karakus@gmail.com', '123asd', '30.00'),
(8, 'deniz', 'tunç', '05301850396', 'tunc.deniz@gmail.com', '123asd', '50.00'),
(9, 'aslı', 'gök', '05325070440', 'gok.asli@gmail.com', '123asd', '100.00'),
(10, 'zeki can', 'gözcu', '05321136290', 'gozcu.zeki@gmail.com', '123asd', '0.00');

--
-- Tetikleyiciler `users`
--
DELIMITER $$
CREATE TRIGGER `kullanici_eklendiginde` AFTER INSERT ON `users` FOR EACH ROW INSERT INTO log_records(description, actualized_by, actualized_at) VALUES (
    CONCAT(new.name," ",new.surname," isimli kullanıcı sisteme kaydedildi. ID: ",new.user_id)
    ,NULL,Now())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `kullanici_guncellendiginde` AFTER UPDATE ON `users` FOR EACH ROW INSERT INTO log_records(description, actualized_by, actualized_at) VALUES (
    CONCAT(new.name," ",new.surname," isimli kullanıcının bilgileri değiştirildi. ID: ",new.user_id)
    ,NULL,Now())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `user_courses`
--

CREATE TABLE `user_courses` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `user_courses`
--

INSERT INTO `user_courses` (`id`, `user_id`, `course_id`) VALUES
(1, 1, 8),
(2, 2, 3),
(3, 3, 5),
(4, 4, 2),
(5, 5, 1),
(6, 5, 6),
(7, 6, 6),
(8, 7, 7),
(9, 8, 4),
(10, 9, 11),
(11, 9, 10);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `user_roles`
--

CREATE TABLE `user_roles` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Tablo döküm verisi `user_roles`
--

INSERT INTO `user_roles` (`id`, `user_id`, `role_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 2),
(4, 4, 3),
(5, 5, 3),
(6, 6, 3),
(7, 7, 4),
(8, 8, 4),
(9, 9, 4),
(10, 10, 4);

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `addresses`
--
ALTER TABLE `addresses`
  ADD PRIMARY KEY (`address_id`),
  ADD KEY `address_fk` (`user_id`);

--
-- Tablo için indeksler `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Tablo için indeksler `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`course_id`),
  ADD KEY `instructor_fk` (`instructor_id`);

--
-- Tablo için indeksler `course_categories`
--
ALTER TABLE `course_categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ccategories_course` (`course_id`),
  ADD KEY `ccategories_category` (`category_id`);

--
-- Tablo için indeksler `deleted_courses`
--
ALTER TABLE `deleted_courses`
  ADD PRIMARY KEY (`course_id`);

--
-- Tablo için indeksler `log_records`
--
ALTER TABLE `log_records`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `act_fk` (`actualized_by`);

--
-- Tablo için indeksler `price_average_of_courses`
--
ALTER TABLE `price_average_of_courses`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`);

--
-- Tablo için indeksler `total_courses`
--
ALTER TABLE `total_courses`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email_uk` (`email`);

--
-- Tablo için indeksler `user_courses`
--
ALTER TABLE `user_courses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ucourses_user` (`user_id`),
  ADD KEY `ucourses_course` (`course_id`);

--
-- Tablo için indeksler `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `uroles_user` (`user_id`),
  ADD KEY `uroles_role` (`role_id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `course_categories`
--
ALTER TABLE `course_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Tablo için AUTO_INCREMENT değeri `log_records`
--
ALTER TABLE `log_records`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Tablo için AUTO_INCREMENT değeri `price_average_of_courses`
--
ALTER TABLE `price_average_of_courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `total_courses`
--
ALTER TABLE `total_courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Tablo için AUTO_INCREMENT değeri `user_courses`
--
ALTER TABLE `user_courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Tablo için AUTO_INCREMENT değeri `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `addresses`
--
ALTER TABLE `addresses`
  ADD CONSTRAINT `address_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Tablo kısıtlamaları `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `instructor_fk` FOREIGN KEY (`instructor_id`) REFERENCES `users` (`user_id`);

--
-- Tablo kısıtlamaları `course_categories`
--
ALTER TABLE `course_categories`
  ADD CONSTRAINT `ccategories_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`),
  ADD CONSTRAINT `ccategories_course` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`);

--
-- Tablo kısıtlamaları `log_records`
--
ALTER TABLE `log_records`
  ADD CONSTRAINT `act_fk` FOREIGN KEY (`actualized_by`) REFERENCES `users` (`user_id`);

--
-- Tablo kısıtlamaları `user_courses`
--
ALTER TABLE `user_courses`
  ADD CONSTRAINT `ucourses_course` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  ADD CONSTRAINT `ucourses_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Tablo kısıtlamaları `user_roles`
--
ALTER TABLE `user_roles`
  ADD CONSTRAINT `uroles_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`),
  ADD CONSTRAINT `uroles_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
