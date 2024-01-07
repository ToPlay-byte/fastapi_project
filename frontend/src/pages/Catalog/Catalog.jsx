import styles from './styles.module.css'
import Layout from 'components/layouts/BaseLayout/BaseLayout' 



const Catalog = () => {
    return (
        <Layout>
            <main className="main">
                <aside className={styles['sidbar']}>

                </aside>
                <section className={styles["catalog"]}>
                    <div className="inner">
                        
                    </div>
                </section>
            </main>
        </Layout>
    )
}

export default Catalog 
