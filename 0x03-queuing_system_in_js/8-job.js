import { createQueue } from 'kue'

const queue = createQueue();

const createPushNotificationsJobs = (jobs, queue) => {
	if (!Array.isArray(jobs)) {
		throw new Error('Jobs is not an array');
		return;
	}
	jobs.forEach(obj => {
		const job = queue.create('push_notification_code_3', obj)
					.on('complete', () => {
						console.log(`Notification job created: ${job.id}`);
					})
					.on('failed', (err) => {
						console.log(`Notification job ${job.id} failed: ${err}`);
					})
					.on('progress', (progress) => {
						console.log(`Notification job ${job.id} ${progress}%`);
					})
					.save(() => {
						console.log(`Notification job created: ${job.id}`);
					});
	});
};

export default createPushNotificationsJobs;
