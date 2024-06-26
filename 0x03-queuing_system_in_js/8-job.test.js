import { createQueue } from 'kue'
import createPushNotificationsJobs from './8-job'
import { expect } from 'chai'
import { spy } from 'sinon'

const queue = createQueue();

describe('createPushNotificationsJobs', () => {
	let consoleSpy;

	before(() => {
		queue.testMode.enter();
		consoleSpy = spy(console, 'log');
	});

	afterEach(() => {
		queue.testMode.clear();
	});

	after(() => {
		queue.testMode.exit();
		consoleSpy.restore();
	});

	it('should throw error', () => {
		const jobs = 'not an array';
		expect(() => createPushNotificationsJobs(jobs, queue)).to.throw(Error, 'Jobs is not an array');
		// Log for failed job
		expect(consoleSpy.calledWith(/Notification job \d+ completed/));
	});

	it('should create a job for each obj', () => {
		const jobs = [
			{ title: 'Test Job 1' },
			{ title: 'Test Job 2' }
		]

		createPushNotificationsJobs(jobs, queue);
		expect(queue.testMode.jobs.length).to.equal(jobs.length);
	});

	it('should log appropriate messages', () => {
		const jobs = [
			{ title: 'Test Job 1' },
		]

		createPushNotificationsJobs(jobs, queue);

		// Log for when job is created
		expect(consoleSpy.calledWith(/Notification job created: \d+/));
		// Log for when job is completed
		expect(consoleSpy.calledWith(/Notification job \d+ completed/));
		// Log for progress on job
		expect(consoleSpy.calledWith(/Notification job \d+% complete/));
	});
});
