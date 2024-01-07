import { BiSolidUser, BiSearch } from 'react-icons/bi'
import styles from './style.module.css' 


const Layout = ({children}) => {
    return (
        <>
            <header className={styles["header"]}>
                <div className={styles["wrapper"]}>
                    <div className={styles["header__inner"]}>
                        <div className={styles["logo"]}>
                            <a href="/" className={styles["logo__link"]}>Солнце Европы</a>
                        </div>
                        <form action="/" method='GET' className={styles["header__search"]}>
                            <input className={styles['header__search-input']} type="text" />
                            <button className={styles['header__search-btn']}><BiSearch /></button>
                        </form>
                        <ul className={styles['header__menu']}>
                            <li className={styles["header__user"]}>
                                <a href="/login" className={styles["header__user-link"]}>
                                    <BiSolidUser size={30}/>
                                    <p className={styles["header__user-text"]}>Войти</p>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </header>
            {children}
            <footer className={styles["footer"]}>
                <div className={styles["wrapper"]}>
                    <div className={styles["footer__inner"]}>
                        <div className={styles["footer__contacts"]}>
                            <a href="mailto:oleksandr.hnylosyr@gmail.com" className={styles["footer__link"]}>oleksandr.hnylosyr@gmail.com</a>
                            <a href="tel:380734409269" className={styles['footer__link']}>380734409269</a>
                        </div>
                        <div className={styles["logo"]}>
                            <a href="/" className={styles["logo__link"]}>Солнце Европы</a>
                        </div>
                    </div>
                </div>
            </footer>
        </>
    )
}


export default Layout

