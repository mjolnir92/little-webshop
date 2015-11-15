SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `little_webshop` DEFAULT CHARACTER SET utf8 ;
USE `little_webshop` ;

DROP TABLE IF EXISTS `little_webshop`.`User` ;

CREATE TABLE IF NOT EXISTS `little_webshop`.`User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `firstName` VARCHAR(45) NULL,
  `lastName` VARCHAR(45) NULL,
  `streetAddress` VARCHAR(45) NULL,
  `postCode` INT NULL,
  `postTown` VARCHAR(45) NULL,
  `phoneNr` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `admin` TINYINT(1) NULL,
  PRIMARY KEY (`idUser`),
  UNIQUE INDEX `login_UNIQUE` (`login` ASC))
ENGINE = InnoDB;


DROP TABLE IF EXISTS `little_webshop`.`Category` ;

CREATE TABLE IF NOT EXISTS `little_webshop`.`Category` (
  `idCategory` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCategory`),
  UNIQUE INDEX `categoryName_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


DROP TABLE IF EXISTS `little_webshop`.`Asset` ;

CREATE TABLE IF NOT EXISTS `little_webshop`.`Asset` (
  `idAsset` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `price` FLOAT NULL,
  `amount` INT NULL,
  `imagePath` VARCHAR(200) NULL,
  `Category_idCategory` INT NOT NULL,
  PRIMARY KEY (`idAsset`),
  INDEX `fk_Asset_AssetCategory1_idx` (`Category_idCategory` ASC),
  CONSTRAINT `fk_Asset_AssetCategory1`
    FOREIGN KEY (`Category_idCategory`)
    REFERENCES `little_webshop`.`Category` (`idCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


DROP TABLE IF EXISTS `little_webshop`.`Order` ;

CREATE TABLE IF NOT EXISTS `little_webshop`.`Order` (
  `idOrder` INT NOT NULL AUTO_INCREMENT,
  `dateTime` DATETIME NULL,
  `status` INT NULL,
  `User_idUser` INT NOT NULL,
  PRIMARY KEY (`idOrder`),
  INDEX `fk_Order_Customer_idx` (`User_idUser` ASC),
  CONSTRAINT `fk_Order_Customer`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `little_webshop`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


DROP TABLE IF EXISTS `little_webshop`.`OrderRow` ;

CREATE TABLE IF NOT EXISTS `little_webshop`.`OrderRow` (
  `idOrderRow` INT NOT NULL AUTO_INCREMENT,
  `amount` INT NULL,
  `Order_idOrder` INT NOT NULL,
  `Asset_idAsset` INT NOT NULL,
  PRIMARY KEY (`idOrderRow`),
  INDEX `fk_OrderItem_Order1_idx` (`Order_idOrder` ASC),
  INDEX `fk_OrderItem_Asset1_idx` (`Asset_idAsset` ASC),
  CONSTRAINT `fk_OrderItem_Order1`
    FOREIGN KEY (`Order_idOrder`)
    REFERENCES `little_webshop`.`Order` (`idOrder`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_OrderItem_Asset1`
    FOREIGN KEY (`Asset_idAsset`)
    REFERENCES `little_webshop`.`Asset` (`idAsset`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
