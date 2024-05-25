import type { NextPage } from 'next';
import { useCallback } from 'react';
import styles from './index.module.css';


const MacBookPro14:NextPage = () => {
  	
  	const onGroupContainerClick = useCallback(() => {
    		// Add your code here
  	}, []);
  	
  	return (
    		<div className={styles.macbookPro141}>
      			<img className={styles.messageimage1713698813764CopIcon} alt="" src="messageImage_1713698813764_copy-removebg-preview 1.png" />
      			<div className={styles.macbookPro141Child} />
      			<div className={styles.letsSeeHow}>Let’s see how it’s works !</div>
      			<div className={styles.squashMachineSimulatorContainer}>
        				<p className={styles.squashMachine}>{`Squash Machine `}</p>
        				<p className={styles.squashMachine}>{`Simulator `}</p>
      			</div>
      			<div className={styles.vectorParent} onClick={onGroupContainerClick}>
        				<img className={styles.groupChild} alt="" src="Rectangle 2.svg" />
        				<b className={styles.start}>Start</b>
      			</div>
    		</div>);
};

export default MacBookPro14;
