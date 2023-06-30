-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 25, 2023 at 01:25 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1securecrimedb`
--

-- --------------------------------------------------------

--
-- Table structure for table `crimenaltb`
--

CREATE TABLE `crimenaltb` (
  `id` bigint(10) NOT NULL auto_increment,
  `CriminalId` varchar(250) NOT NULL,
  `Name` varchar(250) NOT NULL,
  `Height` varchar(250) NOT NULL,
  `Weight` varchar(250) NOT NULL,
  `Mole` varchar(250) NOT NULL,
  `Colour` varchar(250) NOT NULL,
  `CrimeInfo` varchar(500) NOT NULL,
  `CrimeFile` varchar(500) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `crimenaltb`
--

INSERT INTO `crimenaltb` (`id`, `CriminalId`, `Name`, `Height`, `Weight`, `Mole`, `Colour`, `CrimeInfo`, `CrimeFile`) VALUES
(1, 'CRIMRNALID001', 'san', '6.5', '65', 'face', 'white', 'sdfsd', '32.png'),
(2, 'CRIMRNALID003.0', 'siddiq', '6.5', '65', 'face', 'white', 'theft', '32.png'),
(4, 'CRIMRNALID005.0', 'bharath', '6.5', '65', 'leg', 'black', 'hhhghg', 'adminLogin.jpg'),
(5, 'CRIMRNALID006.0', 'emman', '6.5', '56', 'chin', 'brown', 'ijuhu', '123.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `msgtb`
--

CREATE TABLE `msgtb` (
  `id` bigint(10) NOT NULL auto_increment,
  `ReceiverName` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `imageid` varchar(250) NOT NULL,
  `ImageName` varchar(250) NOT NULL,
  `Hidekey` varchar(250) NOT NULL,
  `PupKey` varchar(250) NOT NULL,
  `Privkey` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `msgtb`
--

INSERT INTO `msgtb` (`id`, `ReceiverName`, `Email`, `imageid`, `ImageName`, `Hidekey`, `PupKey`, `Privkey`) VALUES
(1, 'sangeeth', 'sangeeth5535@gmail.com', '8496', '8496.png', '1234', '030dff13006274e0ea1023e913bb6f7c266df2c2f2a462ceb4789c999002b4c5f5', '1c6fa4bc80bdfd1f2f438e05a3a10b2e62d06c004de16382009687e85bbce3c5'),
(2, 'sangeeth', 'sangeeth5535@gmail.com', '1639', '1639.png', '1234', '039bc666b9eed94b69e1cb855ee3d2acfa41a5fc7e309e70f818ce54434198695b', 'c0af8f7ce0e0e640b0a68d9f5b94fd43b047d449004a9b430959ba3766b5d412'),
(3, 'san', 'sangeeth5535@gmail.com', '6168', '6168.png', '1234', '03ad260f19053299de229918626baec06d711c932755015a3c16825f920ed49bac', '2e76665e3d11fff6c98ac607038d115459d8b27988bebb9cc27128e95753f39c'),
(4, 'san5535', 'sangeeth5535@gmail.com', '3304', '3304.png', '1234', '02e438bba6ba74370e515b85632069779bf73ff968c5b54c5e388d65e31aa98b74', '3dbb6f8d10e5eb815c4dcba5e0746a39fca4af4d90f5f7cdf5e6cb473a25209f'),
(5, 'san', 'sangeeth5535@gmail.com', '6653', '6653.png', '0000', '0232e2a3a15e98b2292fff596c2759706873ddebcf0515b1aa6bad803dd632b1bf', '39a9bb53c816cc51714487dd75497955617ae8d34d1efedd5b007bf43e8f94f4'),
(6, 'san', 'sangeeth5535@gmail.com', '5862', '5862.png', '5252', '02910fdb07727a0ba5f22e090680ae9b7fc21e22502dc0ff2751e58d72a775df3e', '13b4372c8fe170075f3c2e0539f74032ab84b7f4328069868897e75e41ba6836'),
(7, 'san', 'sangeeth5535@gmail.com', '5862', '5862.png', '5252', '039acd3db89574edcd82cb632dfec36068b14dafedade9153abb6e355de5074051', 'dfde4f7a11727bc875bb01bef7fd527c3d3c87e056e42a251e7d43975c477708');

-- --------------------------------------------------------

--
-- Table structure for table `recivertb`
--

CREATE TABLE `recivertb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `EmailId` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `recivertb`
--

INSERT INTO `recivertb` (`id`, `Name`, `Mobile`, `EmailId`, `Address`, `UserName`, `Password`) VALUES
(1, 'san', '9486365535', 'sangeeth5535@gmail.com', 'no 6 trichy', 'sangeeth', 'sangeeth'),
(2, 'san', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'san', 'san'),
(3, 'sangeeth Kumar', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'san5535', 'san5535');
